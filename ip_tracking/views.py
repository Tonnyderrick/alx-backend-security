from django.shortcuts import render

# Create your views here.
# ip_tracking/views.py
from django.http import HttpResponse
from ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# For function-based view
@csrf_exempt
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def login_view(request):
    if request.method == 'POST':
        return HttpResponse("Login attempt.")
    return HttpResponse("Login page.")
