from django.shortcuts import render

# Create your views here.
from .models import Components

def components_list(request):
    components = Components.objects.all()
    return render(request, 'pc_build/components_list.html', {'components': components})