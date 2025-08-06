from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from decimal import Decimal 

User = get_user_model()

class PointsPackage(models.Model):
    name = models.CharField(_('package name'), max_length=100)
    name_ar = models.CharField(_('package name (Arabic)'), max_length=100, blank=True)
    points = models.PositiveIntegerField(_('points'))
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EGP')
    discount_percentage = models.PositiveIntegerField(_('discount percentage'), default=0)
    is_popular = models.BooleanField(_('is popular'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Points Package')
        verbose_name_plural = _('Points Packages')
        ordering = ['points']

    def __str__(self):
        return f"{self.name} - {self.points} points"

    @property
    def discounted_price(self):
        if self.discount_percentage > 0:
            return self.price * (Decimal('1') - Decimal(self.discount_percentage) / Decimal('100'))
        return self.price
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('accepted', _('Accepted')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
        ('disputed', _('Disputed')),
    ]

    # Parties
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_as_seller')
    skill = models.ForeignKey('skills.Skill', on_delete=models.CASCADE, related_name='skill_orders')
    
    # Order details
    points_amount = models.PositiveIntegerField(_('points amount'))
    platform_fee = models.PositiveIntegerField(_('platform fee'))
    total_points = models.PositiveIntegerField(_('total points'))
    
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    requirements = models.TextField(_('requirements'), blank=True)
    delivery_notes = models.TextField(_('delivery notes'), blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    accepted_at = models.DateTimeField(_('accepted at'), null=True, blank=True)
    started_at = models.DateTimeField(_('started at'), null=True, blank=True)
    completed_at = models.DateTimeField(_('completed at'), null=True, blank=True)
    cancelled_at = models.DateTimeField(_('cancelled at'), null=True, blank=True)
    
    # Delivery
    expected_delivery = models.DateTimeField(_('expected delivery'), null=True, blank=True)
    actual_delivery = models.DateTimeField(_('actual delivery'), null=True, blank=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['buyer', 'status']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.skill.title}"

    def calculate_platform_fee(self):
        """Calculate platform fee based on points amount"""
        from django.conf import settings
        fee_percentage = getattr(settings, 'PLATFORM_FEE_PERCENTAGE', 8)
        return int(self.points_amount * fee_percentage / 100)

    def save(self, *args, **kwargs):
        if not self.platform_fee:
            self.platform_fee = self.calculate_platform_fee()
        if not self.total_points:
            self.total_points = self.points_amount + self.platform_fee
        super().save(*args, **kwargs)

class PointsTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', _('Purchase')),
        ('earned', _('Earned')),
        ('spent', _('Spent')),
        ('refund', _('Refund')),
        ('bonus', _('Bonus')),
        ('penalty', _('Penalty')),
    ]

    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('cancelled', _('Cancelled')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points_transactions')
    transaction_type = models.CharField(_('transaction type'), max_length=20, choices=TRANSACTION_TYPES)
    amount = models.IntegerField(_('amount'))  # Can be negative for spent/penalty
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Related objects - using string references to avoid circular imports
    skill = models.ForeignKey('skills.Skill', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey('points.Order', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Additional info
    description = models.CharField(_('description'), max_length=200, blank=True)
    reference_id = models.CharField(_('reference ID'), max_length=100, blank=True)
    payment_id = models.CharField(_('payment ID'), max_length=100, blank=True)  # Store payment ID as string
    
    # Balance tracking
    balance_before = models.PositiveIntegerField(_('balance before'))
    balance_after = models.PositiveIntegerField(_('balance after'))
    
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('Points Transaction')
        verbose_name_plural = _('Points Transactions')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'transaction_type']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.transaction_type} - {self.amount} points"
