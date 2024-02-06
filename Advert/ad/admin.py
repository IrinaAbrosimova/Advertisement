from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Ad, Rating, StarRating, MediaFile, Review, Author

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Ad
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', "get_image")
    list_display_links = ("name",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ("text", )


class MediaFileInline(admin.TabularInline):
    model = MediaFile
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
        list_display = ("id", "title", "category", "poster", "draft", "created_date", "modified_date")
        list_filter = ("category", "published_date")
        search_fields = ("title", "description", "category__name")
        inlines = [MediaFileInline, ReviewInline]
        save_on_top = True
        save_as = True
        list_editable = ("draft",)
        actions = ["publish", "unpublish"]
        form = AdAdminForm
        readonly_fields = ("get_image",)
        fieldsets = (
            (None, {
                "fields": (("title", "author"),)
            }),
            (None, {
                "fields": ("category", "poster", "description")
            }),
            (None, {
                "fields": (("draft"),)
            }),
            (None, {
                "fields": (("published_date"),)
            }),

        )

        def get_image(self, obj):
            return mark_safe(f'<img src={obj.poster.url} width="50" height="60"')

        def unpublish(self, request, queryset):
            row_update = queryset.update(draft=True)
            if row_update == 1:
                message_bit = "1 запись была обновлена"
            else:
                message_bit = f"{row_update} записей были обновлены"
            self.message_user(request, f"{message_bit}")

        def publish(self, request, queryset):
            row_update = queryset.update(draft=False)
            if row_update == 1:
                message_bit = "1 запись была обновлена"
            else:
                message_bit = f"{row_update} записей были обновлены"
            self.message_user(request, f"{message_bit}")

        publish.short_description = "Опубликовать"
        publish.allowed_permissions = ('change',)

        unpublish.short_description = "Снять с публикации"
        unpublish.allowed_permissions = ('change',)

        get_image.short_description = "Изображение"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "user")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("star", "ip")


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ("name", "ad", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


admin.site.register(StarRating)
admin.site.site_title = "MMORPG"
admin.site.site_header = "MMORPG"

