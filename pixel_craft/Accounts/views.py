
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm,RegisterForm

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/') 
            else:
                
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'Accounts/Login.html', {'form': form})
    



def Logout(request):
    logout(request)
    return redirect(Login)
def Register(request):
    if(request.method=='POST'):
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(Login)
        else:
            return render(request,'Accounts/Register.html',{'form':form})
    else:
        form=RegisterForm()
    return render(request,'Accounts/Register.html',{'form':form})
        
        
def Profile(request):
    pass
def Profile_edit(request):
    pass