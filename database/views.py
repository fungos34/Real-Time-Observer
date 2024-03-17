from django.shortcuts import render
from django.http import HttpResponse
from .models import SolMate 

import logging

logger = logging.getLogger(__name__)

def index(request):
    """Handles GET requests to the main url. Redirects to index.html"""
    context = {}
    return render(request, "database/index.html", context=context)