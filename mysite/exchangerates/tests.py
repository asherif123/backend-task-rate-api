import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class RateTests(APITestCase):
    def test_get_rate_from_to_date(self):
        """
        Ensure that the api returns status 200, and correct data, when
        Args Passed To API: from_currency, to_currency, date
        are passed correctly
        """
        url = '/exchangerates/rates/?from_currency=USD&to_currency=GBP&date=2020-09-14'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        correct_data = {
            "from_currency": "USD",
            "to_currency": "GBP",
            "date": datetime.datetime.strptime("2020-09-14", '%Y-%m-%d').date(),
            "exchange_rate": 0.77627
        }
        self.assertEqual(response.data, correct_data)

    def test_get_rate_from_to(self):
        """
        Ensure that the api returns status 200, when
        Args Passed To API: from_currency, to_currency, without date
        are passed correctly

        Ensure that the api returns today's date as
        there is no date provided
        """
        url = '/exchangerates/rates/?from_currency=USD&to_currency=GBP'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        date = datetime.date.today()
        self.assertEqual(response.data['date'], date)

    def test_get_rate_missing_arg_from(self):
        """
        Ensure that the api returns bad request 400, and
        specifies the missing arg when
        Args Passed To API: from_currency is not provided
        """
        url = '/exchangerates/rates/?to_currency=GBP'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'required_parameter': 'from_currency'})

    def test_get_rate_missing_arg_to(self):
        """
        Ensure that the api returns bad request 400, and
        specifies the missing arg when
        Args Passed To API: to_currency is not provided
        """
        url = '/exchangerates/rates/?from_currency=USD'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'required_parameter': 'to_currency'})

    def test_get_rate_missing_args(self):
        """
        Ensure that the api returns bad request 400, when no Args are provided
        """
        url = '/exchangerates/rates/?'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        self.assertEqual(response.data, {'required_parameter': 'from_currency'})

    def test_get_rate_wrong_currency(self):
        """
        Ensure that the api returns status 404, when
        Args Passed To API: from_currency, and/or to_currency
        are not correct
        """
        url = '/exchangerates/rates/?from_currency=EGP&to_currency=GBP&date=2020-09-14'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = '/exchangerates/rates/?from_currency=EGP&to_currency=GBPP&date=2020-09-14'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = '/exchangerates/rates/?from_currency=USD&to_currency=EGP&date=2020-09-14'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_rate_date_from_future(self):
        """
        Ensure that the api returns status 200,
        and today's date when there is future date provided
        Args Passed To API: from_currency, to_currency, future_date
        """
        date = datetime.date.today() + datetime.timedelta(days=5)
        url = '/exchangerates/rates/?from_currency=USD&to_currency=GBP&date={}'.format(
            date.strftime('%Y-%m-%d'))
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        date = datetime.date.today()
        self.assertEqual(response.data['date'], date)
