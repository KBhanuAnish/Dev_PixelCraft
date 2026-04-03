from django.shortcuts import render

# Create your views here.
from .models import Component

def components_list(request):
    components = Component.objects.all()
    return render(request, 'pc_build/components_list.html', {'components': components})