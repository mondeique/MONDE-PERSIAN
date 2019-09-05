from django.contrib import admin
from category_data.models import *
# Register your models here.

admin.site.register(MyUser)
admin.site.register(OriginalImage)
admin.site.register(CroppedImage)
admin.site.register(ColorTag)
admin.site.register(ShapeTag)
admin.site.register(CharmTag)
admin.site.register(HandleTag)
admin.site.register(DecoTag)
admin.site.register(PatternTag)
admin.site.register(Categories)

