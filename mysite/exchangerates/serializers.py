from exchangerates.models import Rate
from rest_framework import serializers


class RateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rate
        fields = ['from_currency', 'to_currency', 'exchange_rate']
        extra_kwargs = {'from_currency': {'required': True}}
        