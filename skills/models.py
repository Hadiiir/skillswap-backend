from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    name_ar = models.CharField(_('name (Arabic)'), max_length=100, blank=True)
    description = models.TextField(_('description'), blank=True)
    description_ar = models.TextField(_('description (Arabic)'), blank=True)
    icon = models.CharField(_('icon'), max_length=50, blank=True)  # Font Awesome icon class
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class Skill(models.Model):
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('ar', _('Arabic')),
        ('both', _('Both')),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
    ]

    STATUS_CHOICES = [
        ('active', _('Active')),
        ('paused', _('Paused')),
        ('completed', _('Completed')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='skills')
    
    title = models.CharField(_('title'), max_length=200)
    title_ar = models.CharField(_('title (Arabic)'), max_length=200, blank=True)
    description = models.TextField(_('description'))
    description_ar = models.TextField(_('description (Arabic)'), blank=True)
    
    # Pricing and Details
    points_required = models.PositiveIntegerField(_('points required'))
    estimated_duration = models.CharField(_('estimated duration'), max_length=100)  # e.g., "2 hours", "1 week"
    language = models.CharField(_('language'), max_length=10, choices=LANGUAGE_CHOICES, default='en')
    difficulty = models.CharField(_('difficulty'), max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    
    # Media
    thumbnail = models.ImageField(_('thumbnail'), upload_to='skills/thumbnails/', blank=True, null=True)
    video_intro = models.URLField(_('video introduction'), blank=True)
    
    # Status and Stats
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(_('is featured'), default=False)
    total_orders = models.PositiveIntegerField(_('total orders'), default=0)
    average_rating = models.DecimalField(_('average rating'), max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(_('total reviews'), default=0)
    
    # SEO and Tags
    tags = models.CharField(_('tags'), max_length=500, blank=True, help_text=_('Comma-separated tags'))
    meta_description = models.CharField(_('meta description'), max_length=160, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Skill')
        verbose_name_plural = _('Skills')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['points_required']),
            models.Index(fields=['average_rating']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title

    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    def update_rating(self):
        """Update skill's average rating based on reviews"""
        from reviews.models import Review
        reviews = Review.objects.filter(skill=self)
        if reviews.exists():
            self.average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.total_reviews = reviews.count()
            self.save(update_fields=['average_rating', 'total_reviews'])

class SkillImage(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_('image'), upload_to='skills/images/')
    caption = models.CharField(_('caption'), max_length=200, blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Skill Image')
        verbose_name_plural = _('Skill Images')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.skill.title} - Image {self.order}"

class SkillFAQ(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(_('question'), max_length=300)
    question_ar = models.CharField(_('question (Arabic)'), max_length=300, blank=True)
    answer = models.TextField(_('answer'))
    answer_ar = models.TextField(_('answer (Arabic)'), blank=True)
    order = models.PositiveIntegerField(_('order'), default=0)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Skill FAQ')
        verbose_name_plural = _('Skill FAQs')
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.skill.title} - {self.question[:50]}"
