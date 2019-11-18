from django.contrib import admin
from category_data.models import *
from django import forms
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.urls import path


class CsvImportForm(forms.Form):
    csv_file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))


class OriginalImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_url']

    def get_urls(self):
        urls = [path('admin_import_csv/', self.import_csv, name='source_import_csv'),]
        urls += super().get_urls()
        return urls

    def import_csv(self, request):
        if request.method == 'GET':
            ctx = {
                'form': CsvImportForm(),
            }
            return render(request, 'working_page/csv_form.html', ctx)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


# class ColorAdmin(admin.ModelAdmin):
#     list_display = ['id', 'color_name']


class ShapeAdmin(admin.ModelAdmin):
    list_display = ['id', 'shape_name']


class CoverAdmin(admin.ModelAdmin):
    list_display = ['id', 'cover_name']

# class HandleAdmin(admin.ModelAdmin):
#     list_display = ['id', 'handle_name']


class CharmAdmin(admin.ModelAdmin):
    list_display = ['id', 'charm_name']


# class DecoAdmin(admin.ModelAdmin):
#     list_display = ['id', 'deco_name']


class PatternAdmin(admin.ModelAdmin):
    list_display = ['id', 'pattern_name']


admin.site.register(MyUser)
admin.site.register(OriginalImage, OriginalImageAdmin)
admin.site.register(CroppedImage)
# admin.site.register(ColorTag, ColorAdmin)
admin.site.register(ShapeTag, ShapeAdmin)
admin.site.register(CoverTag, CoverAdmin)
# admin.site.register(HandleTag, HandleAdmin)
admin.site.register(CharmTag, CharmAdmin)
# admin.site.register(DecoTag, DecoAdmin)
admin.site.register(PatternTag, PatternAdmin)
admin.site.register(Categories)

