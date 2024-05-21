from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Order(models.Model):
    user= models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    num_word=models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5000)],
        default=0,
        help_text="عدد صحیح با مقدار حداقل 0 و حداکثر 5000."
    )
    CONTENT_CHOICES = [
        ('landing', 'لندینگ'),
        ('product_description', 'توضیح محصول'),
        ('article', 'مقاله'),
        ('reportage', 'رپورتاژ'),
    ]

    typ_content= models.CharField(
        max_length=50,
        choices=CONTENT_CHOICES,
        default='landing',  # مقدار پیشفرض اختیاری
        help_text="یکی از گزینه‌های لندینگ، توضیح محصول، مقاله یا رپورتاژ را انتخاب کنید."
    )
    CONTENT_CHOICES_level = [
        ('simple_content', 'ساده'),
        ('Semi-specialized_content', 'محتوا نیمه تخصصی'),
        ('Specialized_content', 'محتوای تخصصی'),
    ]
    level_content= models.CharField(
        max_length=50,
        choices=CONTENT_CHOICES_level,
        default='simple_content',  # مقدار پیشفرض اختیاری
        help_text="یکی از گزینه‌های ساده، محتوا نیمه تخصصی، محتوا تخصصی را انتخاب کنید."
    )
    title= models.CharField(max_length = 180)
    keyword= models.CharField(max_length = 180)
    body= models.TextField()
    image = models.ImageField(default='defalt.jpg', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    admin_uploade_file = models.FileField(upload_to='orders/')


    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[0:100] + " ..."

# class WordDocument(models.Model):
#     document = models.FileField(upload_to='word_documents/')


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    uploaded_file = models.FileField(upload_to='documents/')
    admin_uploade_file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title
    # For images, you'd use ImageField() instead
    # uploaded_image = models.ImageField(upload_to='images/')

