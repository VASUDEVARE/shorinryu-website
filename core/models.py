"""
Models for Shorin Ryu Karate Do India
Every model here = one section you manage in Django Admin.
"""
from django.db import models
from django_resized import ResizedImageField


# ─────────────────────────────────────────────────────────────────────────────
# 1. SITE SETTINGS  (Edit your phone, email, address from Admin panel)
# ─────────────────────────────────────────────────────────────────────────────
class SiteSettings(models.Model):
    """
    Global site settings — only ONE row allowed.
    Edit from Admin → Site Settings.
    """
    site_name       = models.CharField(max_length=200, default="Shorin Ryu Karate Do India")
    tagline         = models.CharField(max_length=300, default="Traditional • Sports • Martial Arts")
    phone           = models.CharField(max_length=20, blank=True)
    whatsapp        = models.CharField(max_length=20, blank=True, help_text="Number with country code e.g. 919844232681")
    email           = models.EmailField(blank=True)
    address         = models.TextField(blank=True)
    city            = models.CharField(max_length=100, default="Ongole")
    state           = models.CharField(max_length=100, default="Andhra Pradesh")
    google_maps_embed = models.TextField(blank=True, help_text="Paste full Google Maps iframe embed code here")
    # Social Links
    facebook        = models.URLField(blank=True)
    instagram       = models.URLField(blank=True)
    youtube         = models.URLField(blank=True)
    twitter         = models.URLField(blank=True)
    linkedin        = models.URLField(blank=True)
    # Training Hours
    morning_hours   = models.CharField(max_length=100, default="6:00 AM – 8:00 AM")
    evening_hours   = models.CharField(max_length=100, default="5:00 PM – 8:00 PM")
    working_days    = models.CharField(max_length=100, default="Monday – Saturday")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def save(self, *args, **kwargs):
        # Enforce singleton — only one SiteSettings row
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ─────────────────────────────────────────────────────────────────────────────
# 2. HOME PAGE — Hero stats + Testimonials
# ─────────────────────────────────────────────────────────────────────────────
class Testimonial(models.Model):
    name        = models.CharField(max_length=100)
    label       = models.CharField(max_length=150, help_text="e.g. Parent of Student • 3 Years")
    review      = models.TextField()
    stars       = models.IntegerField(default=5, choices=[(i,i) for i in range(1,6)])
    is_active   = models.BooleanField(default=True)
    order       = models.IntegerField(default=0, help_text="Lower number = shown first")

    class Meta:
        ordering = ['order']
        verbose_name = "Testimonial / Review"

    def __str__(self):
        return f"{self.name} ({self.stars}★)"


# ─────────────────────────────────────────────────────────────────────────────
# 3. ABOUT — Sensei profile
# ─────────────────────────────────────────────────────────────────────────────
class Sensei(models.Model):
    name        = models.CharField(max_length=100)
    title       = models.CharField(max_length=200, help_text="e.g. Chief Instructor • WKF Licensed")
    rank        = models.CharField(max_length=100, help_text="e.g. 4th Dan Black Belt")
    photo       = ResizedImageField(
                    size=[500, 500], crop=['middle', 'center'],
                    upload_to='instructors/', blank=True, null=True)
    bio = models.TextField()
    quote       = models.TextField(blank=True, help_text="Personal quote / motto")
    wkf_license = models.BooleanField(default=True, verbose_name="WKF Licensed Coach")
    ace_cert    = models.BooleanField(default=False, verbose_name="ACE Certified Trainer")
    years_exp   = models.IntegerField(default=0, verbose_name="Years of Experience")
    order       = models.IntegerField(default=0)
    is_chief    = models.BooleanField(default=False, verbose_name="Is Chief Instructor")

    class Meta:
        ordering = ['order']
        verbose_name = "Instructor / Sensei"

    def __str__(self):
        return self.name


class SenseiSkill(models.Model):
    sensei      = models.ForeignKey(Sensei, on_delete=models.CASCADE, related_name='skills')
    skill_name  = models.CharField(max_length=100, help_text="e.g. Traditional Kata")
    level_label = models.CharField(max_length=50, help_text="e.g. Expert, Advanced")
    percentage  = models.IntegerField(default=80, help_text="0-100 for the skill bar width")

    def __str__(self):
        return f"{self.sensei.name} — {self.skill_name}"


# ─────────────────────────────────────────────────────────────────────────────
# 4. KARATE CLASSES
# ─────────────────────────────────────────────────────────────────────────────
class KarateClass(models.Model):
    CLASS_TYPES = [
        ('traditional', 'Traditional Karate'),
        ('sports',      'Sports Karate'),
        ('selfdefence', 'Self Defence'),
        ('kids',        'Kids Karate'),
        ('fitness',     'Fitness & Conditioning'),
        ('kobudo',      'Kobudo Weapons'),
    ]
    STATUS = [
        ('open',    'Open for Enrollment'),
        ('limited', 'Limited Seats'),
        ('enquire', 'Enquire'),
        ('full',    'Class Full'),
    ]
    name            = models.CharField(max_length=100)
    class_type      = models.CharField(max_length=20, choices=CLASS_TYPES)
    description     = models.TextField()
    icon_emoji      = models.CharField(max_length=10, default='🥋', help_text="Paste an emoji icon")
    age_group       = models.CharField(max_length=100, help_text="e.g. 4 Years & Above")
    level           = models.CharField(max_length=100, help_text="e.g. Beginner to Advanced")
    duration        = models.CharField(max_length=50,  help_text="e.g. 60–90 Minutes")
    standard        = models.CharField(max_length=100, blank=True, help_text="e.g. WKF Licensed, ACE Certified")
    status          = models.CharField(max_length=10, choices=STATUS, default='open')
    is_active       = models.BooleanField(default=True)
    order           = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Karate Class"

    def __str__(self):
        return self.name


class ClassSchedule(models.Model):
    DAYS = [
        ('mon-sat',       'Monday – Saturday'),
        ('mon-wed-fri',   'Mon / Wed / Fri'),
        ('tue-thu-sat',   'Tue / Thu / Sat'),
        ('sat-sun',       'Sat / Sun'),
        ('appointment',   'By Appointment'),
    ]
    karate_class    = models.ForeignKey(KarateClass, on_delete=models.CASCADE, related_name='schedules')
    days            = models.CharField(max_length=30, choices=DAYS)
    morning_time    = models.CharField(max_length=50, blank=True, help_text="e.g. 6:00 AM – 7:30 AM or leave blank")
    evening_time    = models.CharField(max_length=50, blank=True, help_text="e.g. 5:00 PM – 7:00 PM or leave blank")

    def __str__(self):
        return f"{self.karate_class.name} — {self.days}"


# ─────────────────────────────────────────────────────────────────────────────
# 5. GALLERY
# ─────────────────────────────────────────────────────────────────────────────
class GalleryPhoto(models.Model):
    CATEGORIES = [
        ('training',    'Training'),
        ('tournament',  'Tournaments'),
        ('grading',     'Gradings'),
        ('events',      'Events'),
        ('kobudo',      'Kobudo'),
    ]
    title       = models.CharField(max_length=200)
    category    = models.CharField(max_length=20, choices=CATEGORIES, default='training')
    image       = ResizedImageField(
                    size=[1200, 900], quality=85,
                    upload_to='gallery/')
    caption     = models.CharField(max_length=200, blank=True)
    year        = models.CharField(max_length=10, blank=True, help_text="e.g. 2024")
    is_featured = models.BooleanField(default=False)
    order       = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-uploaded_at']
        verbose_name = "Gallery Photo"

    def __str__(self):
        return self.title


# ─────────────────────────────────────────────────────────────────────────────
# 6. BLOG
# ─────────────────────────────────────────────────────────────────────────────
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title           = models.CharField(max_length=300)
    slug            = models.SlugField(unique=True, help_text="URL-friendly version of title e.g. philosophy-of-shorin-ryu")
    category        = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    author          = models.ForeignKey(Sensei, on_delete=models.SET_NULL, null=True, blank=True)
    cover_image     = ResizedImageField(
                        size=[1200, 630], quality=85,
                        upload_to='blogs/', blank=True, null=True)
    icon_emoji      = models.CharField(max_length=10, default='🥋')
    excerpt         = models.TextField(max_length=400, help_text="Short summary shown on blog listing page")
    content         = models.TextField(help_text="Full blog post content — write your article here")
    tags            = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags e.g. karate,shorinryu,kata")
    is_published    = models.BooleanField(default=False, help_text="Tick this to make the post visible on the website")
    created_at      = models.DateTimeField(auto_now_add=True)
    published_at    = models.DateField(null=True, blank=True, help_text="Date to show on post")
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Blog Post"

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]


# ─────────────────────────────────────────────────────────────────────────────
# 7. CONTACT MESSAGES (saved from the contact form)
# ─────────────────────────────────────────────────────────────────────────────
class ContactMessage(models.Model):
    PROGRAMS = [
        ('traditional', 'Traditional Karate'),
        ('sports',      'Sports Karate'),
        ('selfdefence', 'Self Defence'),
        ('kids',        'Kids Karate'),
        ('fitness',     'Fitness & Conditioning'),
        ('oneononone',  'One-on-One Training'),
        ('general',     'General Enquiry'),
    ]
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20, blank=True)
    program     = models.CharField(max_length=20, choices=PROGRAMS, blank=True)
    age_group   = models.CharField(max_length=100, blank=True)
    message     = models.TextField()
    is_read     = models.BooleanField(default=False, verbose_name="Marked as Read")
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at']
        verbose_name = "Contact Message"

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.received_at.strftime('%d %b %Y')}"
