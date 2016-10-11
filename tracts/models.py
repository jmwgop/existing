from django.db import models
from django.conf import settings
from shortuuidfield import ShortUUIDField

class Tract(models.Model):

    LEASED = 'LSE'
    PARTIALLY_LEASED = 'PLSE'
    PURCHASED = 'OWN'
    PARTIALLY_PURCHASED = 'POWN'
    COMPETITIOR = 'CLSE'
    PARTIAL_COMPETITOR = 'PCLSE'
    OPEN = 'OP'
    STATUS_CHOICES = (
        (LEASED, 'Leased'),
        (PARTIALLY_LEASED, 'Partially Leased'),
        (PURCHASED, 'Purchased'),
        (PARTIALLY_PURCHASED, 'Partially Purchased'),
        (COMPETITIOR, 'Competitor'),
        (PARTIAL_COMPETITOR, 'Partial Competitor'),
        (OPEN, 'Open'),
    )

    uuid = ShortUUIDField(unique=True)
    short_legal = models.CharField(max_length=100)
    full_legal = models.TextField()
    situs_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    created_on = models.DateField(auto_now_add=True)
    acreage = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(
        max_length=5,
        choices=STATUS_CHOICES,
        default=OPEN,
    )


    class Meta:
        verbose_name_plural = 'tracts'

    def __unicode__(self):
        return u"%s" % self.name

    @models.permalink
    def get_absolute_url(self):
        return 'tract_detail', [self.uuid]

    @models.permalink
    def get_update_url(self):
        return 'tract_update', [self.uuid]

    @models.permalink
    def get_delete_url(self):
        return 'tract_delete', [self.uuid]
