import time
import psutil
import logging
from django.core.cache import cache
from django.db import connection
from django.conf import settings
from datetime import datetime, timedelta
import json

class PerformanceMonitor:
    """مراقب الأداء المتقدم"""
    
    def __init__(self):
        self.metrics_cache_timeout = 60  # دقيقة واحدة
        self.alert_thresholds = {
            'response_time': 2.0,  # ثانيتان
            'memory_usage': 80,    # 80%
            'cpu_usage': 80,       # 80%
            'db_queries': 50,      # 50 استعلام
            'error_rate': 5        # 5%
        }
    
    def track_request_performance(self, request, response, processing_time):
        """تتبع أداء الطلبات"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'processing_time': processing_time,
            'user_id': request.user.id if request.user.is_authenticated else None,
            'ip_address': self._get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'db_queries': len(connection.queries),
            'memory_usage': self._get_memory_usage(),
            'cpu_usage': self._get_cpu_usage()
        }
        
        # حفظ المقاييس
        self._save_metrics(metrics)
        
        # فحص التنبيهات
        self._check_alerts(metrics)
        
        return metrics
    
    def get_system_health(self):
        """الحصول على صحة النظام"""
        cache_key = "system_health"
        cached_health = cache.get(cache_key)
        
        if cached_health:
            return cached_health
        
        health_data = {
            'timestamp': datetime.now().isoformat(),
            'system': {
                'cpu_usage': self._get_cpu_usage(),
                'memory_usage': self._get_memory_usage(),
                'disk_usage': self._get_disk_usage(),
                'load_average': self._get_load_average()
            },
            'database': {
                'connection_count': self._get_db_connections(),
                'slow_queries': self._get_slow_queries_count(),
                'query_performance': self._get_avg_query_time()
            },
            'cache': {
                'hit_rate': self._get_cache_hit_rate(),
                'memory_usage': self._get_cache_memory_usage()
            },
            'application': {
                'active_users': self._get_active_users_count(),
                'error_rate': self._get_error_rate(),
                'avg_response_time': self._get_avg_response_time()
            }
        }
        
        # تحديد الحالة العامة
        health_data['overall_status'] = self._calculate_overall_health(health_data)
        
        cache.set(cache_key, health_data, self.metrics_cache_timeout)
        return health_data
    
    def get_performance_trends(self, hours=24):
        """الحصول على اتجاهات الأداء"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        # جمع البيانات من الكاش أو قاعدة البيانات
        trends = {
            'response_times': self._get_response_time_trend(start_time, end_time),
            'error_rates': self._get_error_rate_trend(start_time, end_time),
            'user_activity': self._get_user_activity_trend(start_time, end_time),
            'resource_usage': self._get_resource_usage_trend(start_time, end_time)
        }
        
        return trends
    
    def _get_client_ip(self, request):
        """الحصول على IP العميل"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _get_memory_usage(self):
        """الحصول على استخدام الذاكرة"""
        memory = psutil.virtual_memory()
        return round(memory.percent, 2)
    
    def _get_cpu_usage(self):
        """الحصول على استخدام المعالج"""
        return round(psutil.cpu_percent(interval=1), 2)
    
    def _get_disk_usage(self):
        """الحصول على استخدام القرص الصلب"""
        disk = psutil.disk_usage('/')
        return round(disk.percent, 2)
    
    def _get_load_average(self):
        """الحصول على متوسط الحمولة"""
        try:
            return psutil.getloadavg()[0]  # 1-minute load average
        except:
            return 0
    
    def _get_db_connections(self):
        """عدد اتصالات قاعدة البيانات"""
        # يمكن تنفيذ هذا بناءً على نوع قاعدة البيانات
        return len(connection.queries)
    
    def _get_slow_queries_count(self):
        """عدد الاستعلامات البطيئة"""
        slow_queries = [q for q in connection.queries if float(q['time']) > 1.0]
        return len(slow_queries)
    
    def _get_avg_query_time(self):
        """متوسط وقت الاستعلامات"""
        if not connection.queries:
            return 0
        
        total_time = sum(float(q['time']) for q in connection.queries)
        return round(total_time / len(connection.queries), 4)
    
    def _get_cache_hit_rate(self):
        """معدل نجاح الكاش"""
        # يمكن تنفيذ هذا بناءً على نوع الكاش المستخدم
        return 85.5  # مؤقت
    
    def _get_cache_memory_usage(self):
        """استخدام ذاكرة الكاش"""
        return 45.2  # مؤقت
    
    def _get_active_users_count(self):
        """عدد المستخدمين النشطين"""
        from django.contrib.auth import get_user_model
        from django.utils import timezone
        
        User = get_user_model()
        last_hour = timezone.now() - timedelta(hours=1)
        return User.objects.filter(last_active__gte=last_hour).count()
    
    def _get_error_rate(self):
        """معدل الأخطاء"""
        # يمكن حساب هذا من سجلات الأخطاء
        return 2.1  # مؤقت
    
    def _get_avg_response_time(self):
        """متوسط وقت الاستجابة"""
        cache_key = "avg_response_time"
        return cache.get(cache_key, 0.5)
    
    def _save_metrics(self, metrics):
        """حفظ المقاييس"""
        # حفظ في قاعدة البيانات أو ملف السجل
        cache_key = f"metrics_{int(time.time())}"
        cache.set(cache_key, metrics, 3600)  # ساعة واحدة
        
        # يمكن أيضاً إرسال إلى خدمات مراقبة خارجية
        self._send_to_monitoring_service(metrics)
    
    def _send_to_monitoring_service(self, metrics):
        """إرسال المقاييس لخدمة مراقبة خارجية"""
        # يمكن إرسال إلى Datadog, New Relic, إلخ
        pass
    
    def _check_alerts(self, metrics):
        """فحص التنبيهات"""
        alerts = []
        
        if metrics['processing_time'] > self.alert_thresholds['response_time']:
            alerts.append({
                'type': 'slow_response',
                'message': f"Slow response time: {metrics['processing_time']}s",
                'severity': 'warning'
            })
        
        if metrics['memory_usage'] > self.alert_thresholds['memory_usage']:
            alerts.append({
                'type': 'high_memory',
                'message': f"High memory usage: {metrics['memory_usage']}%",
                'severity': 'critical'
            })
        
        if metrics['db_queries'] > self.alert_thresholds['db_queries']:
            alerts.append({
                'type': 'too_many_queries',
                'message': f"Too many DB queries: {metrics['db_queries']}",
                'severity': 'warning'
            })
        
        # إرسال التنبيهات
        for alert in alerts:
            self._send_alert(alert)
    
    def _send_alert(self, alert):
        """إرسال تنبيه"""
        # يمكن إرسال عبر البريد الإلكتروني، Slack، إلخ
        logging.warning(f"Performance Alert: {alert['message']}")
    
    def _calculate_overall_health(self, health_data):
        """حساب الحالة العامة للنظام"""
        scores = []
        
        # نقاط الأداء
        if health_data['system']['cpu_usage'] < 70:
            scores.append(100)
        elif health_data['system']['cpu_usage'] < 85:
            scores.append(70)
        else:
            scores.append(30)
        
        if health_data['system']['memory_usage'] < 70:
            scores.append(100)
        elif health_data['system']['memory_usage'] < 85:
            scores.append(70)
        else:
            scores.append(30)
        
        if health_data['application']['error_rate'] < 1:
            scores.append(100)
        elif health_data['application']['error_rate'] < 5:
            scores.append(70)
        else:
            scores.append(30)
        
        avg_score = sum(scores) / len(scores)
        
        if avg_score >= 90:
            return 'excellent'
        elif avg_score >= 70:
            return 'good'
        elif avg_score >= 50:
            return 'fair'
        else:
            return 'poor'

# مراقب الأداء
performance_monitor = PerformanceMonitor()
