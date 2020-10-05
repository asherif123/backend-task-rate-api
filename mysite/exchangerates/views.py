import datetime

import requests
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from exchangerates.models import Rate
from exchangerates.serializers import RateSerializer


def get_exchange_rate(date, from_currency, to_currency):
    """
    Calls the frankfurter API to get the exchange rate

    Args:
        date (datetime.date): The first parameter
        from_currency (string): The second parameter
        to_currency (string): The third parameter

    Returns:
        float: if successful, None otherwise.
    """
    url = "https://api.frankfurter.app/{}".format(date.strftime('%Y-%m-%d'))
    parameters = {'from': from_currency, 'to': to_currency}

    response = requests.get(url=url, params=parameters)
    if response.status_code == 200:
        rate = response.json()['rates'][to_currency]
    else:
        rate = None
    return rate

class RateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ViewSet for API that responds with the exchange rate between
    two currencies on a particular date
    """

    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, format=None):
        """
        Returns exchange rate.

        Args(query_parameters):
            from_currency (string): The first parameter
            to_currency (string): The second parameter
            date (string): The third parameter (optional)

        Returns(JSON):
            from_currency (string)
            to_currency (string)
            date (string)
            exchange_rate (float)
        """
        from_currency = request.query_params.get('from_currency', None)
        to_currency = request.query_params.get('to_currency', None)
        date = request.query_params.get('date', None)

        # Validate the API's query parameters
        if from_currency is None:
            return Response({'required_parameter': 'from_currency'},
                status=status.HTTP_400_BAD_REQUEST)
        if to_currency is None:
            return Response({'required_parameter': 'to_currency'},
                status=status.HTTP_400_BAD_REQUEST)
        # Optional parameter, defaults to today if not specified
        if date is None:
            date = datetime.date.today()
        else:
            # Create date object from the input date string
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            # Make sure that date is not in the future
            if date > datetime.date.today():
                date = datetime.date.today()

        # Check if we already have the required exchange rate in DB
        stored_exchange_rate = Rate.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
            exchange_rate_date=date).first()

        # exchange_rate was not stored in DB, fetch it and save it
        if stored_exchange_rate is None:
            exchange_rate = get_exchange_rate(date, from_currency, to_currency)
            if exchange_rate is None:
                return Response({'error': 'url_not_found'},
                    status=status.HTTP_404_NOT_FOUND)
            rate = Rate(
                from_currency=from_currency,
                to_currency=to_currency,
                exchange_rate=exchange_rate,
                exchange_rate_date=date)
            rate.save()
        else:
            exchange_rate = stored_exchange_rate.exchange_rate

        return Response({'from_currency': from_currency,
                        'to_currency': to_currency,
                        'date': date,
                        'exchange_rate': exchange_rate})
