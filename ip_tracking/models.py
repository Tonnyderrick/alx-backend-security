from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address} accessed {self.path} at {self.timestamp} from {self.city}, {self.country}"


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address
