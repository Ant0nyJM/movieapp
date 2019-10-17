from django.contrib import admin

# Register your models here.
from .models import MotionPicture,Artist,Rate,Review,List,Category,CategoryLabel

admin.site.register(MotionPicture)
admin.site.register(Artist)
admin.site.register(Rate)
admin.site.register(Review)
admin.site.register(List)
admin.site.register(Category)
admin.site.register(CategoryLabel)