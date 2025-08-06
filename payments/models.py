from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('paymob', 'Paymob'),
        ('vodafone_cash', 'Vodafone Cash'),
        ('etisalat_cash', 'Etisalat Cash'),
        ('orange_cash', 'Orange Cash'),
    ]

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('processing', _('Processing')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
        ('refunded', _('Refunded')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    points_package = models.ForeignKey('points.PointsPackage', on_delete=models.CASCADE)
    
    # Payment details
    amount = models.DecimalField(_('amount'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EGP')
    payment_method = models.CharField(_('payment method'), max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # External references
    external_payment_id = models.CharField(_('external payment ID'), max_length=200, blank=True)
    external_reference = models.CharField(_('external reference'), max_length=200, blank=True)
    
    # Metadata
    metadata = models.JSONField(_('metadata'), default=dict, blank=True)
    failure_reason = models.TextField(_('failure reason'), blank=True)
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} - {self.user.full_name} - {self.amount} {self.currency}"
