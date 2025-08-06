from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    skill = models.ForeignKey('skills.Skill', on_delete=models.CASCADE, related_name='reviews')
    order = models.OneToOneField('points.Order', on_delete=models.CASCADE, related_name='order_review')
    
    rating = models.PositiveIntegerField(
        _('rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(_('comment'), blank=True)
    
    # Review aspects
    communication_rating = models.PositiveIntegerField(
        _('communication rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    quality_rating = models.PositiveIntegerField(
        _('quality rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    delivery_rating = models.PositiveIntegerField(
        _('delivery rating'),
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    
    is_public = models.BooleanField(_('is public'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']
        unique_together = ['reviewer', 'order']

    def __str__(self):
        return f"Review by {self.reviewer.full_name} for {self.skill.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update skill and user ratings
        self.skill.update_rating()
        self.reviewee.update_rating()
