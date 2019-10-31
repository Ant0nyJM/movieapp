from django.contrib import admin

# Register your models here.
from .models import MotionPicture,Artist,Rate,Review,List,Category,CategoryLabel

class MotionPictureAdmin(admin.ModelAdmin):
    list_display = ('name','release_date','genre','get_director')



class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name','birthday','artist_type','modified_date_time')

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
admin.site.register(Category)
admin.site.register(CategoryLabel)