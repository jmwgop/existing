from django.db import models
from django.conf import settings
from shortuuidfield import ShortUUIDField

class Tracts(models.Model):
    uuid = ShortUUIDField(unique=True)
    short_legal = models.CharField(max_length=100)
    full_legal = models.TextField(blank=True)
    situs_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_on = models.DateField(auto_now_add=True)
    gid = models.IntegerField()

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
