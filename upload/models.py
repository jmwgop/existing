from django.db import models
from django.utils import timezone
from django.conf import settings
from .validators import validate_file_extension

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d/%s', validators=[validate_file_extension])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    created = models.DateTimeField(auto_now_add=True)

class RunReq(models.Model):
    pull_id = models.AutoField(primary_key=True)
    landman = models.IntegerField()
    document_count = models.IntegerField()
    created = models.DateTimeField()

class RunRequestDocs(models.Model):
    pull_id = models.IntegerField()
    volume = models.CharField(max_length=4)
    page = models.CharField(max_length=4)
    rec_type = models.CharField(max_length=4)
    year = models.CharField(max_length=4)
    inst_num = models.CharField(max_length=20)
