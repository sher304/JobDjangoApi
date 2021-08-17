from django.contrib import admin

from django.contrib import admin


from .models import *


class CodeImageInline(admin.TabularInline):
    model = CodeImage
    max_num = 10


@admin.register(Ads)
class ProblemAdmin(admin.ModelAdmin):
    inlines = [CodeImageInline, ]


admin.site.register(Rating)
admin.site.register(Reply)
admin.site.register(RatingStar)
