from django.contrib import admin
from .models import Product, Currency, Topic, Comment, User, Listed, Role

admin.site.register(Listed)
admin.site.register(Role)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Currency)
admin.site.register(Topic)
admin.site.register(Comment)
