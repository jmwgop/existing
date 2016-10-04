from django.db import models

class ConstantIndex(models.Model):
    models.IntegerField()
    doc_type = models.CharField(max_length=20)
    file_date = models.DateTimeField()
    instrument_date = models.DateTimeField()

class GrantorIndex(models.Model):
    models.IntegerField()
    grantor = models.CharField(max_length=40)

class GranteeIndex(models.Model):
    vp_index_id = models.IntegerField()
    grantee = models.CharField(max_length=40)

class ImgIndex(models.Model):
    vp_index_id = models.IntegerField()
    img_path = models.CharField(max_length=200)

class LegalIndex(models.Model):
    vp_index_id = models.IntegerField()
    legal = models.CharField(max_length=45)
    plss_block = models.CharField(max_length=15)
    plss_block_ext = models.CharField(max_length=8)
    plss_section = models.CharField(max_length=15)
    addition_name = models.CharField(max_length=40)
    lot_number = models.CharField(max_length=6)
    lot_number_upper = models.CharField(max_length=6)
    block = models.CharField(max_length=6)
    plat_cabinet = models.CharField(max_length=6)
    plat_page = models.CharField(max_length=6)

class VpDoc(models.Model):
    vp_index_id = models.IntegerField()
    volume = models.CharField(max_length=5)
    page = models.CharField(max_length=4)
    rec_type = models.CharField(max_length=2)
    year = models.IntegerField()
    doc_num = models.IntegerField()
