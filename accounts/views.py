from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm


# Create your views here.
def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, password=password, username=username)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            # attempts = request.session.get('attempts') or 0
            # request.session['attempts'] = attempts + 1
            # TOD: Ban IP after 5 attempts for 24 hours
            request.session['invalid_user'] = 1
        return render(request, "forms.html")


def logout_view(request):
    logout(request)
    redirect('/login')
