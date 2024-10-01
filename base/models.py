from django.contrib.auth.models import AbstractUser
from django.db import models
#
#
class Role(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

class User(AbstractUser):
    name = models.CharField(max_length=120, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default='Seller', null=True)

    avatar = models.ImageField(null=True, upload_to='images', default='/images/avatar.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Currency(models.Model):
    name = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    catogory = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True,null=True)
    # particepents =
    creator = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    price = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='../static/media/images/user.png',blank=True, null=True,upload_to='images/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Listed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created','user']

    def __str__(self):
        return f'{self.body}'

