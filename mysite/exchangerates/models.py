from django.db import models

# TODO: ADD DOCSTRING


# Create your models here.
class Rate(models.Model):
    """
    Stores a single rate entry
    """
    from_currency = models.CharField(max_length=6)
    to_currency = models.CharField(max_length=6)
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=10, default=None)
    exchange_rate_date = models.DateField()

    def __str__(self):
        return '{0} to {1}={2}'.format(self.from_currency, \
            self.to_currency, self.exchange_rate)
