"""
Admin Panel Configuration — Shorin Ryu Karate Do India
Everything you manage via /admin/ is configured here.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Testimonial, Sensei, SenseiSkill,
    KarateClass, ClassSchedule, GalleryPhoto,
    BlogCategory, BlogPost, ContactMessage
)


# ─────────────────────────────────────────────────────────────────────────────
# SITE SETTINGS
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🏫 School Information', {
            'fields': ('site_name', 'tagline', 'city', 'state', 'address')
        }),
        ('📞 Contact Details', {
            'fields': ('phone', 'whatsapp', 'email')
        }),
        ('🕐 Training Hours', {
            'fields': ('working_days', 'morning_hours', 'evening_hours')
        }),
        ('🌐 Social Media Links', {
            'fields': ('facebook', 'instagram', 'youtube', 'twitter', 'linkedin')
        }),
        ('🗺️ Google Maps', {
            'fields': ('google_maps_embed',),
            'description': 'Go to Google Maps → search your address → Share → Embed a Map → copy full iframe code'
        }),
    )

    def has_add_permission(self, request):
        # Only allow one settings object
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ─────────────────────────────────────────────────────────────────────────────
# TESTIMONIALS
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ('name', 'label', 'stars', 'is_active', 'order')
    list_editable = ('is_active', 'order', 'stars')
    list_filter   = ('is_active', 'stars')
    ordering      = ('order',)


# ─────────────────────────────────────────────────────────────────────────────
# INSTRUCTORS / SENSEI
# ─────────────────────────────────────────────────────────────────────────────
class SenseiSkillInline(admin.TabularInline):
    model  = SenseiSkill
    extra  = 3
    fields = ('skill_name', 'level_label', 'percentage')


@admin.register(Sensei)
class SenseiAdmin(admin.ModelAdmin):
    list_display  = ('name', 'title', 'rank', 'is_chief', 'order', 'photo_preview')
    list_editable = ('order', 'is_chief')
    inlines       = [SenseiSkillInline]
    fieldsets = (
        ('👤 Basic Info', {
            'fields': ('name', 'title', 'rank', 'photo', 'is_chief', 'order')
        }),
        ('📝 Biography', {
            'fields': ('bio', 'quote')
        }),
        ('🏅 Certifications', {
            'fields': ('wkf_license', 'ace_cert', 'years_exp')
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:50px;height:50px;border-radius:50%;object-fit:cover;"/>', obj.photo.url)
        return "No photo"
    photo_preview.short_description = "Photo"


# ─────────────────────────────────────────────────────────────────────────────
# KARATE CLASSES
# ─────────────────────────────────────────────────────────────────────────────
class ClassScheduleInline(admin.TabularInline):
    model  = ClassSchedule
    extra  = 1


@admin.register(KarateClass)
class KarateClassAdmin(admin.ModelAdmin):
    list_display  = ('name', 'class_type', 'age_group', 'duration', 'status', 'is_active', 'order')
    list_editable = ('status', 'is_active', 'order')
    list_filter   = ('class_type', 'status', 'is_active')
    inlines       = [ClassScheduleInline]


# ─────────────────────────────────────────────────────────────────────────────
# GALLERY
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'year', 'is_featured', 'order', 'image_preview')
    list_editable = ('category', 'is_featured', 'order')
    list_filter   = ('category', 'is_featured')
    ordering      = ('order', '-uploaded_at')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:80px;height:60px;object-fit:cover;border-radius:4px;"/>', obj.image.url)
        return "No image"
    image_preview.short_description = "Preview"


# ─────────────────────────────────────────────────────────────────────────────
# BLOG
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display    = ('title', 'category', 'author', 'is_published', 'published_at')
    list_editable   = ('is_published',)
    list_filter     = ('is_published', 'category', 'author')
    search_fields   = ('title', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('📰 Post Details', {
            'fields': ('title', 'slug', 'category', 'author', 'icon_emoji', 'published_at')
        }),
        ('🖼️ Cover Image', {
            'fields': ('cover_image',)
        }),
        ('📝 Content', {
            'fields': ('excerpt', 'content', 'tags')
        }),
        ('✅ Publishing', {
            'fields': ('is_published',)
        }),
    )


# ─────────────────────────────────────────────────────────────────────────────
# CONTACT MESSAGES
# ─────────────────────────────────────────────────────────────────────────────
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('first_name', 'last_name', 'email', 'phone', 'program', 'is_read', 'received_at')
    list_editable = ('is_read',)
    list_filter   = ('program', 'is_read')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'program', 'age_group', 'message', 'received_at')

    # Cannot add or delete messages from admin — only view and mark as read
    def has_add_permission(self, request):
        return False
