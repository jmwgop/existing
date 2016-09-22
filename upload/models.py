from django.db import models
from django.utils import timezone
from .validators import validate_file_extension

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d/%s', validators=[validate_file_extension])
