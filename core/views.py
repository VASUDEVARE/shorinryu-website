"""
Views for Shorin Ryu Karate Do India
Each function = one page on the website.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Testimonial, Sensei, KarateClass,
    GalleryPhoto, BlogPost, BlogCategory, ContactMessage
)
from .forms import ContactForm


# ─── HOME ─────────────────────────────────────────────────────────────────────
def home(request):
    context = {
        'testimonials': Testimonial.objects.filter(is_active=True),
        'classes':      KarateClass.objects.filter(is_active=True)[:4],
        'gallery':      GalleryPhoto.objects.filter(is_featured=True)[:6],
    }
    return render(request, 'home.html', context)


# ─── ABOUT ────────────────────────────────────────────────────────────────────
def about(request):
    context = {
        'chief_sensei': Sensei.objects.filter(is_chief=True).first(),
        'all_sensei':   Sensei.objects.all(),
    }
    return render(request, 'about.html', context)


# ─── INSTRUCTORS ──────────────────────────────────────────────────────────────
def instructors(request):
    context = {
        'instructors': Sensei.objects.all().prefetch_related('skills'),
    }
    return render(request, 'instructors.html', context)


# ─── CLASSES ──────────────────────────────────────────────────────────────────
def classes(request):
    context = {
        'classes': KarateClass.objects.filter(is_active=True).prefetch_related('schedules'),
    }
    return render(request, 'classes.html', context)


# ─── GALLERY ──────────────────────────────────────────────────────────────────
def gallery(request):
    cat    = request.GET.get('cat', 'all')
    photos = GalleryPhoto.objects.all()
    if cat != 'all':
        photos = photos.filter(category=cat)
    context = {
        'photos':       photos,
        'active_cat':   cat,
        'categories':   GalleryPhoto.CATEGORIES,
    }
    return render(request, 'gallery.html', context)


# ─── CONTACT ──────────────────────────────────────────────────────────────────
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            # Send email notification to site owner
            try:
                send_mail(
                    subject=f"New Enquiry from {msg.first_name} {msg.last_name}",
                    message=(
                        f"Name: {msg.first_name} {msg.last_name}\n"
                        f"Email: {msg.email}\n"
                        f"Phone: {msg.phone}\n"
                        f"Program: {msg.get_program_display()}\n"
                        f"Age Group: {msg.age_group}\n\n"
                        f"Message:\n{msg.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass  # Don't crash if email fails; message is already saved to DB

            messages.success(request, "Thank you! Your message has been received. We will contact you within 24 hours.")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# ─── BLOGS ────────────────────────────────────────────────────────────────────
def blogs(request):
    cat_slug    = request.GET.get('category', '')
    posts       = BlogPost.objects.filter(is_published=True)
    active_cat  = None

    if cat_slug:
        active_cat = get_object_or_404(BlogCategory, slug=cat_slug)
        posts = posts.filter(category=active_cat)

    context = {
        'posts':        posts,
        'categories':   BlogCategory.objects.all(),
        'active_cat':   active_cat,
        'recent_posts': BlogPost.objects.filter(is_published=True)[:5],
        'all_tags':     _get_all_tags(),
    }
    return render(request, 'blogs/list.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    context = {
        'post':         post,
        'recent_posts': BlogPost.objects.filter(is_published=True).exclude(pk=post.pk)[:5],
        'categories':   BlogCategory.objects.all(),
    }
    return render(request, 'blogs/detail.html', context)


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def _get_all_tags():
    """Collect all unique tags from all published blog posts."""
    all_tags = set()
    for post in BlogPost.objects.filter(is_published=True):
        for tag in post.get_tags_list():
            all_tags.add(tag)
    return sorted(all_tags)
