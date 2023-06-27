from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html
from django.templatetags.static import static
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [
        'get_image_list_preview',
        'title',
        'is_active',
    ]
    list_display_links = [
        'title',
    ]
    readonly_fields = [
        'get_image_preview',
    ]
    prepopulated_fields = {'slug': ('title',)}

    class Media:
        css = {
            "all": (
                static("admin/foodcartapp.css")
            )
        }

    def get_image_preview(self, obj):
        if not obj.image:
            return 'выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
    get_image_preview.short_description = 'превью'

    def get_image_list_preview(self, obj):
        if not obj.image or not obj.id:
            return 'нет картинки'
        edit_url = reverse('admin:banners_banner_change', args=(obj.id,))
        return format_html('<a href="{edit_url}"><img src="{src}" style="max-height: 50px;"/></a>', edit_url=edit_url, src=obj.image.url)
    get_image_list_preview.short_description = 'превью'
