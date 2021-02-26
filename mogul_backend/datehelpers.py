from django.utils import timezone

def one_day_ago():
    return timezone.now() + timezone.timedelta(days=-1)

def one_hour_ago():
    return timezone.now() + timezone.timedelta(hours=-1)