from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password"""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(_('bio'), max_length=500, blank=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)
    location = models.CharField(_('location'), max_length=100, blank=True)
    website = models.URLField(_('website'), blank=True)
    
    # Points and Rating
    points_balance = models.PositiveIntegerField(_('points balance'), default=100)
    total_earned_points = models.PositiveIntegerField(_('total earned points'), default=0)
    total_spent_points = models.PositiveIntegerField(_('total spent points'), default=0)
    rating = models.DecimalField(_('rating'), max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(_('total reviews'), default=0)
    
    # Account Status
    is_verified = models.BooleanField(_('is verified'), default=False)
    is_premium = models.BooleanField(_('is premium'), default=False)
    premium_expires = models.DateTimeField(_('premium expires'), blank=True, null=True)
    
    # Preferences
    preferred_language = models.CharField(
        _('preferred language'),
        max_length=5,
        choices=[('en', 'English'), ('ar', 'Arabic')],
        default='en'
    )
    email_notifications = models.BooleanField(_('email notifications'), default=True)
    push_notifications = models.BooleanField(_('push notifications'), default=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    last_active = models.DateTimeField(_('last active'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def update_rating(self):
        """Update user's average rating based on reviews"""
        from reviews.models import Review
        reviews = Review.objects.filter(skill__user=self)
        if reviews.exists():
            self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.total_reviews = reviews.count()
            self.save(update_fields=['rating', 'total_reviews'])

class UserSkill(models.Model):
    """Skills that a user possesses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    name = models.CharField(_('skill name'), max_length=100)
    level = models.CharField(
        _('skill level'),
        max_length=20,
        choices=[
            ('beginner', _('Beginner')),
            ('intermediate', _('Intermediate')),
            ('advanced', _('Advanced')),
            ('expert', _('Expert'))
        ],
        default='beginner'
    )
    years_of_experience = models.PositiveIntegerField(_('years of experience'), default=0)
    is_verified = models.BooleanField(_('is verified'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('User Skill')
        verbose_name_plural = _('User Skills')
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.user.full_name} - {self.name}"
