from django.contrib import admin
from category_data.models import *
# Register your models here.


class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'color_name']


class ShapeAdmin(admin.ModelAdmin):
    list_display = ['id', 'shape_name']


class HandleAdmin(admin.ModelAdmin):
    list_display = ['id', 'handle_name']


class CharmAdmin(admin.ModelAdmin):
    list_display = ['id', 'charm_name']


class DecoAdmin(admin.ModelAdmin):
    list_display = ['id', 'deco_name']


class PatternAdmin(admin.ModelAdmin):
    list_display = ['id', 'pattern_name']


admin.site.register(MyUser)
admin.site.register(OriginalImage)
admin.site.register(CroppedImage)
admin.site.register(ColorTag, ColorAdmin)
admin.site.register(ShapeTag, ShapeAdmin)
admin.site.register(HandleTag, HandleAdmin)
admin.site.register(CharmTag, CharmAdmin)
admin.site.register(DecoTag, DecoAdmin)
admin.site.register(PatternTag, PatternAdmin)
admin.site.register(Categories)

