
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,RegisterForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from Vendors.models import Vendor

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # 🔥 Check if user is a vendor
                if Vendor.objects.filter(user=user).exists():
                    return redirect('/vendors/')   # vendor dashboard
                else:
                    return redirect('/')           # normal user homepage

            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'Accounts/Login.html', {'form': form})


def Logout(request):
    logout(request)
    return redirect(Login)

from Vendors.models import Vendor
def Register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            if form.cleaned_data['is_vendor']:
                Vendor.objects.create(
                    user=user,
                    shop_name=user.username  
                )

            return redirect('Login')
    else:
        form = RegisterForm()
    return render(request, 'Accounts/Register.html', {'form': form})

        
def Profile(request):
    pass
def Profile_edit(request):
    pass