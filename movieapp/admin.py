from django.contrib import admin

# Register your models here.
from .models import (Artist, List, MotionPicture,
                     Rate, Review)


class MotionPictureAdmin(admin.ModelAdmin):
    list_display = ('name','release_date','genre','movie_id','get_director')



class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name','birthday','artist_type','artist_id','modified_date_time')

class ListAdmin(admin.ModelAdmin):
    list_display = ('name','user')

class RateAdmin(admin.ModelAdmin):
    list_display = ('__str__','user','movie','rating')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('__str__','user','movie')

admin.site.register(MotionPicture,MotionPictureAdmin)
admin.site.register(Artist,ArtistAdmin)
admin.site.register(Rate,RateAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(List,ListAdmin)
