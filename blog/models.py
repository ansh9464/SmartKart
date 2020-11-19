from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Blogpost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50,default="")
    head0 = models.CharField(max_length=500,default="")
    chead0 = models.CharField(max_length=5000,default="")
    head1 = models.CharField(max_length=500,default="")
    chead1 = models.CharField(max_length=5000,default="")
    head2 = models.CharField(max_length=500,default="")
    chead2 = RichTextUploadingField()
    pub_date = models.DateField("Published Date:")
    thumbnail = models.ImageField(upload_to="shop/images",default="")


    def __str__(self):
        return self.title

class Contactus(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default='')
    email = models.CharField(max_length=30,default='')
    phone = models.CharField(max_length=30,default='')
    desc = models.TextField()

    def __str__(self):
        return  'message from '+ self.email