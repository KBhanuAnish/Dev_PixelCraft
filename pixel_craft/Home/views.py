from django.shortcuts import render
from Accounts.decorators import *
# Create your views here.
@ordinary_user_required
def Home(request):
    return render(request,'Home/Home.html')