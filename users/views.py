from django.shortcuts import redirect, render
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from .models import CustomUser
from recipes.models import Recipes
from .forms import UpdateUserForm


@login_required
def home(request):
    return render(request, 'recipes/home.html')


def logout_attempt(request):
    logout(request)
    return redirect('home')


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = CustomUser.objects.filter(email=username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('login')

        if not user_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login')

        login(request, user)
        return redirect('home')

    return render(request, 'users/login.html')


def register_attempt(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        city = request.POST.get('city')
        description = request.POST.get('description')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).first():
            messages.success(request, 'Email is taken.')
            return redirect('login')

        email_token = str(uuid.uuid4())
        user_obj = CustomUser(email=email, email_token=email_token, first_name=first_name, last_name=last_name, city=city, description=description)
        user_obj.set_password(password)
        user_obj.save()

        send_mail_after_registration(email, email_token)
        return redirect('token_send')

    return render(request, 'users/register.html')


def token_send(request):
    return render(request, 'users/token_send.html')


def verify(request, email_token):
    try:
        user_obj = CustomUser.objects.filter(email_token=email_token).first()

        if user_obj:
            if user_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            user_obj.is_verified = True
            user_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        return redirect('error')


def error_page(request):
    return render(request, 'users/error.html')


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/user/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


class UserUpdate(generic.UpdateView):
    form_class = UpdateUserForm
    template_name = 'users/update_profile.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('user_profile')

    def get_object(self):
        pk = None
        slug = None

        return self.request.user


class UserProfile(generic.DetailView):
    model = CustomUser
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super(UserProfile, self).get_context_data(**kwargs)

        recipes = Recipes.objects.filter(creator=self.request.user.id)

        context_data['recipes'] = recipes
        return context_data
