import hashlib
import hmac
import time
import json
import requests
from datetime import datetime, timedelta
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import logging
import random
import string
import re
from django.contrib.auth.models import AnonymousUser

User = get_user_model()
logger = logging.getLogger(__name__)

class AdvancedSecurityService:
    """Advanced security features for SkillSwap"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.max_login_attempts = 5
        self.lockout_duration = 30  # minutes
    
    def check_rate_limit(self, user_ip, action='login', max_attempts=5, window_minutes=15):
        """Check if user has exceeded rate limit for an action"""
        try:
            cache_key = f"rate_limit_{action}_{user_ip}"
            attempts = cache.get(cache_key, 0)
            
            if attempts >= max_attempts:
                return False, f"Too many {action} attempts. Try again later."
            
            # Increment attempts
            cache.set(cache_key, attempts + 1, timeout=window_minutes * 60)
            return True, "OK"
            
        except Exception as e:
            self.logger.error(f"Error checking rate limit: {e}")
            return True, "OK"  # Allow on error
    
    def detect_suspicious_activity(self, user, request):
        """Detect suspicious user activity"""
        try:
            suspicious_indicators = []
            
            # Check for unusual login times
            current_hour = timezone.now().hour
            if current_hour < 6 or current_hour > 23:
                suspicious_indicators.append("unusual_login_time")
            
            # Check for multiple IP addresses
            user_ip = self.get_client_ip(request)
            recent_ips_key = f"user_ips_{user.id}"
            recent_ips = cache.get(recent_ips_key, set())
            
            if isinstance(recent_ips, set):
                recent_ips.add(user_ip)
            else:
                recent_ips = {user_ip}
            
            if len(recent_ips) > 3:  # More than 3 IPs in recent activity
                suspicious_indicators.append("multiple_ips")
            
            cache.set(recent_ips_key, recent_ips, timeout=24 * 60 * 60)  # 24 hours
            
            # Check for rapid successive actions
            action_key = f"user_actions_{user.id}"
            recent_actions = cache.get(action_key, [])
            current_time = timezone.now().timestamp()
            
            # Remove old actions (older than 5 minutes)
            recent_actions = [
                action_time for action_time in recent_actions 
                if current_time - action_time < 300
            ]
            
            if len(recent_actions) > 20:  # More than 20 actions in 5 minutes
                suspicious_indicators.append("rapid_actions")
            
            recent_actions.append(current_time)
            cache.set(action_key, recent_actions, timeout=300)  # 5 minutes
            
            return suspicious_indicators
            
        except Exception as e:
            self.logger.error(f"Error detecting suspicious activity: {e}")
            return []
    
    def validate_password_strength(self, password):
        """Validate password strength"""
        try:
            errors = []
            
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long")
            
            if not re.search(r"[A-Z]", password):
                errors.append("Password must contain at least one uppercase letter")
            
            if not re.search(r"[a-z]", password):
                errors.append("Password must contain at least one lowercase letter")
            
            if not re.search(r"\d", password):
                errors.append("Password must contain at least one digit")
            
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                errors.append("Password must contain at least one special character")
            
            # Check against common passwords
            common_passwords = [
                'password', '123456', 'password123', 'admin', 'qwerty',
                'letmein', 'welcome', 'monkey', '1234567890'
            ]
            
            if password.lower() in common_passwords:
                errors.append("Password is too common")
            
            return len(errors) == 0, errors
            
        except Exception as e:
            self.logger.error(f"Error validating password: {e}")
            return True, []  # Allow on error
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        except Exception as e:
            self.logger.error(f"Error getting client IP: {e}")
            return "unknown"
    
    def log_security_event(self, event_type, user, request, details=None):
        """Log security events"""
        try:
            user_ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
            
            log_data = {
                'event_type': event_type,
                'user_id': user.id if user and not isinstance(user, AnonymousUser) else None,
                'user_ip': user_ip,
                'user_agent': user_agent,
                'timestamp': timezone.now().isoformat(),
                'details': details or {}
            }
            
            self.logger.warning(f"Security Event: {log_data}")
            
            # Store in cache for recent events
            events_key = "recent_security_events"
            recent_events = cache.get(events_key, [])
            recent_events.append(log_data)
            
            # Keep only last 100 events
            if len(recent_events) > 100:
                recent_events = recent_events[-100:]
            
            cache.set(events_key, recent_events, timeout=24 * 60 * 60)  # 24 hours
            
        except Exception as e:
            self.logger.error(f"Error logging security event: {e}")
    
    def generate_secure_token(self, length=32):
        """Generate a secure random token"""
        try:
            import secrets
            return secrets.token_urlsafe(length)
        except Exception as e:
            self.logger.error(f"Error generating secure token: {e}")
            return hashlib.sha256(str(timezone.now().timestamp()).encode()).hexdigest()[:length]
    
    def _get_client_ip(self, request):
        """Get client IP address from request"""
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        except Exception as e:
            self.logger.error(f"Error getting client IP: {e}")
            return "unknown"
    
    def _get_ip_location(self, ip):
        """Get geographical location of IP address"""
        try:
            cache_key = f"ip_location_{ip}"
            location_info = cache.get(cache_key)
            
            if location_info is None:
                try:
                    # Use a free service to get location
                    response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data['status'] == 'success':
                            location_info = {
                                'country': data.get('country', ''),
                                'city': data.get('city', ''),
                                'region': data.get('regionName', ''),
                                'timezone': data.get('timezone', ''),
                                'lat': data.get('lat', 0),
                                'lon': data.get('lon', 0)
                            }
                        else:
                            location_info = {}
                    else:
                        location_info = {}
                    
                    # Save in cache for 24 hours
                    cache.set(cache_key, location_info, 86400)
                    
                except Exception as e:
                    self.logger.error(f"Error getting IP location: {e}")
                    location_info = {}
            
            return location_info
            
        except Exception as e:
            self.logger.error(f"Error getting IP location: {e}")
            return {}
    
    def _is_unusual_location(self, user, location_info):
        """Check if user's location is unusual"""
        if not location_info:
            return False
        
        cache_key = f"user_locations_{user.id}"
        user_locations = cache.get(cache_key, [])
        
        current_country = location_info.get('country', '')
        
        # If this is the first login
        if not user_locations:
            user_locations.append(current_country)
            cache.set(cache_key, user_locations, 86400 * 30)
            return False
        
        # If the country is new
        if current_country and current_country not in user_locations:
            user_locations.append(current_country)
            cache.set(cache_key, user_locations, 86400 * 30)
            return True
        
        return False
    
    def _is_unusual_user_agent(self, user, user_agent):
        """Check if user's user agent is unusual"""
        cache_key = f"user_agents_{user.id}"
        user_agents = cache.get(cache_key, set())
        
        # Simplify user agent for comparison
        simplified_ua = self._simplify_user_agent(user_agent)
        
        if simplified_ua not in user_agents:
            user_agents.add(simplified_ua)
            cache.set(cache_key, user_agents, 86400 * 7)  # 7 days
            return len(user_agents) > 3  # Suspicious if more than 3 devices
        
        return False
    
    def _simplify_user_agent(self, user_agent):
        """Simplify user agent for comparison"""
        if 'Chrome' in user_agent:
            return 'Chrome'
        elif 'Firefox' in user_agent:
            return 'Firefox'
        elif 'Safari' in user_agent:
            return 'Safari'
        elif 'Edge' in user_agent:
            return 'Edge'
        else:
            return 'Other'
    
    def _is_unusual_time(self, user):
        """Check if user's login time is unusual"""
        current_hour = timezone.now().hour
        
        cache_key = f"user_activity_hours_{user.id}"
        activity_hours = cache.get(cache_key, [])
        
        activity_hours.append(current_hour)
        
        # Keep last 50 hours of activity
        if len(activity_hours) > 50:
            activity_hours = activity_hours[-50:]
        
        cache.set(cache_key, activity_hours, 86400 * 7)
        
        # If we have enough data
        if len(activity_hours) > 10:
            # Calculate usual hours
            hour_counts = {}
            for hour in activity_hours:
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
            
            # If the current hour is rarely used
            current_count = hour_counts.get(current_hour, 0)
            avg_count = sum(hour_counts.values()) / len(hour_counts)
            
            return current_count < avg_count * 0.3
        
        return False
    
    def _is_rapid_activity(self, user):
        """Check for rapid successive actions"""
        cache_key = f"user_activity_times_{user.id}"
        activity_times = cache.get(cache_key, [])
        
        current_time = time.time()
        activity_times.append(current_time)
        
        # Keep last 10 actions
        if len(activity_times) > 10:
            activity_times = activity_times[-10:]
        
        cache.set(cache_key, activity_times, timeout=3600)  # 1 hour
        
        # Check if there are more than 5 actions in one minute
        if len(activity_times) >= 5:
            recent_activities = [t for t in activity_times if current_time - t < 60]
            return len(recent_activities) >= 5
        
        return False
    
    def _log_activity(self, user, ip, user_agent, suspicious_indicators):
        """Log user activity"""
        try:
            activity_log = {
                'user_id': user.id,
                'ip': ip,
                'user_agent': user_agent,
                'timestamp': timezone.now().isoformat(),
                'suspicious_indicators': suspicious_indicators
            }
            
            # Save to database or log file
            self.logger.info(f"User activity: {json.dumps(activity_log)}")
            
        except Exception as e:
            self.logger.error(f"Error logging activity: {e}")
    
    def _handle_suspicious_activity(self, user, indicators, request):
        """Handle suspicious user activity"""
        try:
            # Send security alert to user
            self._send_security_alert(user, indicators, request)
            
            # Log in security log
            self.log_security_event('suspicious_activity', user, request, {
                'indicators': indicators,
                'ip': self.get_client_ip(request),
                'user_agent': request.META.get('HTTP_USER_AGENT', 'unknown')
            })
            
            # If activity is highly suspicious, temporarily lock the account
            if len(indicators) >= 3:
                self._temporary_lock_account(user, 15)  # 15 minutes
            
        except Exception as e:
            self.logger.error(f"Error handling suspicious activity: {e}")
    
    def _send_security_alert(self, user, indicators, request):
        """Send security alert to user"""
        try:
            ip = self.get_client_ip(request)
            location = self._get_ip_location(ip)
            
            subject = "Security Alert - Suspicious Activity Detected"
            message = f"""
            Hello {user.first_name},
            
            Suspicious activity has been detected on your account:
            
            Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
            IP Address: {ip}
            Location: {location.get('city', '')}, {location.get('country', '')}
            Indicators: {', '.join(indicators)}
            
            If you did not perform this activity, please change your password immediately.
            
            Security Team - SkillSwap
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True
            )
            
        except Exception as e:
            self.logger.error(f"Error sending security alert: {e}")
    
    def _temporary_lock_account(self, user, minutes):
        """Temporarily lock user account"""
        try:
            cache_key = f"account_locked_{user.id}"
            lock_until = timezone.now() + timedelta(minutes=minutes)
            
            cache.set(cache_key, lock_until.isoformat(), timeout=minutes * 60)
            
            # Send notification
            subject = "Your Account Has Been Temporarily Locked"
            message = f"""
            Hello {user.first_name},
            
            Your account has been temporarily locked for {minutes} minutes due to suspicious activity.
            
            Lock will be automatically lifted at: {lock_until.strftime('%Y-%m-%d %H:%M:%S')}
            
            If you believe this is an error, please contact our support team.
            
            Security Team - SkillSwap
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True
            )
            
        except Exception as e:
            self.logger.error(f"Error locking account: {e}")
    
    def is_account_locked(self, user):
        """Check if user account is locked"""
        try:
            cache_key = f"account_locked_{user.id}"
            lock_until_str = cache.get(cache_key)
            
            if lock_until_str:
                lock_until = datetime.fromisoformat(lock_until_str)
                if timezone.now() < lock_until:
                    return True, lock_until
                else:
                    # Remove expired lock
                    cache.delete(cache_key)
            
            return False, None
            
        except Exception as e:
            self.logger.error(f"Error checking account lock: {e}")
            return False, None
    
    def generate_2fa_code(self, user):
        """Generate a 2FA code"""
        try:
            # Generate a 6-digit code
            code = ''.join(random.choices(string.digits, k=6))
            
            # Save code in cache for 5 minutes
            cache_key = f"2fa_code_{user.id}"
            cache.set(cache_key, code, timeout=300)
            
            return code
            
        except Exception as e:
            self.logger.error(f"Error generating 2FA code: {e}")
            return None
    
    def verify_2fa_code(self, user, provided_code):
        """Verify a 2FA code"""
        try:
            cache_key = f"2fa_code_{user.id}"
            stored_code = cache.get(cache_key)
            
            if stored_code and stored_code == provided_code:
                # Delete code after use
                cache.delete(cache_key)
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error verifying 2FA code: {e}")
            return False
    
    def send_2fa_code(self, user, method='email'):
        """Send a 2FA code"""
        try:
            code = self.generate_2fa_code(user)
            
            if not code:
                return False
            
            if method == 'email':
                subject = "Verification Code - SkillSwap"
                message = f"""
                Hello {user.first_name},
                
                Your verification code is: {code}
                
                This code is valid for 5 minutes only.
                
                If you did not request this code, please ignore this message.
                
                Security Team - SkillSwap
                """
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False
                )
                
                return True
            
            # Additional methods like SMS can be added here
            
        except Exception as e:
            self.logger.error(f"Error sending 2FA code: {e}")
            return False
    
    def encrypt_sensitive_data(self, data, key=None):
        """Encrypt sensitive data"""
        try:
            if key is None:
                key = settings.SECRET_KEY
            
            # Simple encryption using HMAC
            data_str = json.dumps(data) if not isinstance(data, str) else data
            signature = hmac.new(
                key.encode(),
                data_str.encode(),
                hashlib.sha256
            ).hexdigest()
            
            return f"{signature}:{data_str}"
            
        except Exception as e:
            self.logger.error(f"Error encrypting data: {e}")
            return None
    
    def decrypt_sensitive_data(self, encrypted_data, key=None):
        """Decrypt sensitive data"""
        try:
            if key is None:
                key = settings.SECRET_KEY
            
            if ':' not in encrypted_data:
                return None
            
            signature, data_str = encrypted_data.split(':', 1)
            
            # Verify signature
            expected_signature = hmac.new(
                key.encode(),
                data_str.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if hmac.compare_digest(signature, expected_signature):
                try:
                    return json.loads(data_str)
                except json.JSONDecodeError:
                    return data_str
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error decrypting data: {e}")
            return None
    
    def get_security_report(self, user, days=30):
        """Generate security report for user"""
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=days)
            
            # Get security data from cache
            cache_key = f"security_report_{user.id}_{days}"
            report = cache.get(cache_key)
            
            if report is None:
                # Login statistics
                login_ips = cache.get(f"user_ips_{user.id}", set())
                login_locations = cache.get(f"user_locations_{user.id}", [])
                user_agents = cache.get(f"user_agents_{user.id}", set())
                
                # Check for suspicious activities
                suspicious_count = 0  # Can be fetched from database
                
                report = {
                    'user_id': user.id,
                    'period': {
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat(),
                        'days': days
                    },
                    'login_security': {
                        'unique_ips': len(login_ips),
                        'unique_locations': len(login_locations),
                        'unique_devices': len(user_agents),
                        'suspicious_activities': suspicious_count
                    },
                    'account_status': {
                        'is_locked': self.is_account_locked(user)[0],
                        'two_factor_enabled': hasattr(user, 'two_factor_enabled') and user.two_factor_enabled,
                        'last_password_change': user.last_login.isoformat() if user.last_login else None
                    },
                    'recommendations': self._get_security_recommendations(user)
                }
                
                # Save in cache for 1 hour
                cache.set(cache_key, report, timeout=3600)
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating security report: {e}")
            return {}
    
    def _get_security_recommendations(self, user):
        """Get security recommendations for user"""
        recommendations = []
        
        try:
            # Check password strength
            if user.last_login and (timezone.now() - user.last_login).days > 90:
                recommendations.append({
                    'type': 'password',
                    'message': 'It is recommended to change your password every 90 days',
                    'priority': 'medium'
                })
            
            # Check 2FA status
            if not (hasattr(user, 'two_factor_enabled') and user.two_factor_enabled):
                recommendations.append({
                    'type': '2fa',
                    'message': 'Enable two-factor authentication for additional security',
                    'priority': 'high'
                })
            
            # Check number of devices
            user_agents = cache.get(f"user_agents_{user.id}", set())
            if len(user_agents) > 5:
                recommendations.append({
                    'type': 'devices',
                    'message': 'A large number of devices are being used, review your device list',
                    'priority': 'medium'
                })
            
            # Check locations
            user_locations = cache.get(f"user_locations_{user.id}", [])
            if len(user_locations) > 3:
                recommendations.append({
                    'type': 'locations',
                    'message': 'Logging in from multiple locations, ensure your account security',
                    'priority': 'low'
                })
            
        except Exception as e:
            self.logger.error(f"Error getting security recommendations: {e}")
        
        return recommendations

# Global instance
security_service = AdvancedSecurityService()
