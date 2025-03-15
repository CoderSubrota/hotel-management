from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.utils.http import  urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from users.models import UserProfile
from users.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from users.forms import DepositForm
from decimal import Decimal


def is_admin(user):
    if user.is_authenticated:
        return user.groups.filter(name='Admin').exists()
    else:
        print(f"User {user} is not authenticated")
        return False
    
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            messages.success(request, 'Registration successful! Please check your inbox to verify your email.')
            return redirect('login-page')
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def activate_account(request, user_id, token):
    try:
        user = UserProfile.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.email_verified=True
            user.save()
            return redirect("login-page")
        else:
            return HttpResponse("<p style='color:red;'>Invalid token</p>")
    except UserProfile.DoesNotExist:
        return HttpResponse("<p style='color:red;'>User not found</p>")
    
            
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist) as e:
        messages.error(request, "Invalid verification link.")
        return redirect("register")
    
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.email_verified:  
                login(request, user)
                return redirect("hotel_list")
            else:
                messages.error(request, "Please verify your email before logging in.")
                return redirect("login-page")
        else:
            messages.error(request, "Invalid username or password.")
            # Re-render the login page with the form and messages
            return render(request, "registration/login.html")  

    else:
        return render(request, "registration/login.html")


# Logout View
@login_required(login_url="login-page")
def logout_user(request):
    logout(request)
    return redirect("login-page")

@login_required(login_url="login-page") 
def deposit(request):
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            # Check if the amount is within the allowed range
            if 50 <= amount <= 300:
                user_profile = request.user
                # Use Decimal for balance
                user_balance = Decimal(user_profile.balance)  # Assuming balance is stored as a Decimal
                user_balance += Decimal(amount)  # Add the deposit amount
                user_profile.balance = user_balance  # Update the user's balance
                user_profile.save()  

                messages.success(request, f'Congratulations! You have successfully deposited ${amount:.2f} to your balance.')
                return redirect('deposit') 
            else:
                messages.error(request, 'Please enter an amount between $50 and $300.')
                return redirect('deposit')    
    else:
        form = DepositForm()

    return render(request, 'registration/deposit.html', {'form': form})
