from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication

def index_tmpl(request):
    return render(request, "index.html", {})


def admin_tmpl(request):
    return render(request, "admin.html", {})