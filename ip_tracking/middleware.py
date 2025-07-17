from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import BlockedIP, RequestLog
import requests

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Block check
        if BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Geolocation (with caching)
        geo_info = cache.get(ip)
        if not geo_info:
            geo_info = self.get_geolocation(ip)
            cache.set(ip, geo_info, timeout=86400)  # Cache for 24 hours

        # Log request
        RequestLog.objects.create(
            ip_address=ip,
            country=geo_info.get("country", ""),
            city=geo_info.get("city", "")
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_geolocation(self, ip):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            return {
                "country": data.get("country", ""),
                "city": data.get("city", "")
            }
        except Exception:
            return {"country": "", "city": ""}
