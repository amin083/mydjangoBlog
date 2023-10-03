from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user= models.ForeignKey(User,default=None ,on_delete=models.CASCADE)
    title= models.CharField(max_length = 180)
    keyword= models.CharField(max_length = 180)
    body= models.TextField()
    image = models.ImageField(default='defalt.jpg', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[0:100] + " ..."

