from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from hotels.models import Hotel, Booking, Review
from  hotels.forms import BookingForm, ReviewForm,HotelForm
from users.models import UserProfile
from django.core.mail import send_mail
from django.contrib import messages
from decimal import Decimal
from datetime import datetime
from hotels.models import Booking, Hotel,Payment
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.conf import settings
from hotels.models import Payment
import stripe
import json
from django.views.decorators.csrf import csrf_exempt


def is_admin(user):
    if user.is_authenticated:
        return user.groups.filter(name='Admin').exists()
    else:
        print(f"User {user} is not authenticated")
        return False
    
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/hotel_info.html', {'hotels': hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    reviews = Review.objects.filter(hotel=hotel)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'reviews': reviews})

@login_required(login_url="login-page") 
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    user = request.user

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")

        number_of_days = (check_out_date - check_in_date).days
        
        hotel_price_per_night = Decimal(hotel.price_per_night)  
        total_price = hotel_price_per_night * Decimal(number_of_days)  

        user_balance = Decimal(user.balance)  

        if user_balance >= total_price:
            user.balance = user_balance - total_price  
            user.save()

            booking = Booking.objects.create(
                user=user,
                hotel=hotel,
                check_in=check_in_date,
                check_out=check_out_date,
                total_price=total_price
            )

            if booking:
                send_mail(
                    "Hotel Booking Confirmation",
                    f"Dear {user.username},\n\nYour booking at {hotel.name} is confirmed!\nCheck-in: {check_in}\nCheck-out: {check_out}\nTotal Price: ${total_price:.2f}\n\nThank you!",
                    "subrotachandra6@gmail.com",
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, f"Your booking has been confirmed for {hotel.name} hotel")
                return redirect("hotel_list")
        else:
            messages.error(request, "You do not have enough balance to book this hotel.")

    return render(request, "hotels/book_hotel.html", {"hotel": hotel})

@login_required(login_url="login-page") 
def add_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    user = request.user

    # Check if the user has booked this hotel
    has_booked = Booking.objects.filter(user=user, hotel=hotel).exists()

    if request.method == "POST" and has_booked:
        rating = int(request.POST.get("rating"))
        comment = request.POST.get("comment")

        # Create a new review
        Review.objects.create(user=user, hotel=hotel, rating=rating, comment=comment)
        
        return redirect("hotel_detail", hotel_id=hotel.id)  

    return render(request, "hotels/add_review.html", {"hotel": hotel, "has_booked": has_booked})

@login_required(login_url="login-page")
@user_passes_test(is_admin, login_url='login-page')
def add_hotel(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hotel_crud') 
    else:
        form = HotelForm()
    return render(request, 'admin/add_hotel.html', {'form': form})

@login_required(login_url="login-page")
@user_passes_test(is_admin, login_url='login-page')
def admin_dashboard(request):
    # Get today's date
    today = timezone.now()   
    # Calculate the date for one week ago and one month ago
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)

    # Number of bookings in the last week
    bookings_last_week = Booking.objects.filter(created_at__gte=last_week).count()

    # Number of bookings in the last month
    bookings_last_month = Booking.objects.filter(created_at__gte=last_month).count()

    # Mostly booked rooms
    mostly_booked_rooms = Hotel.objects.annotate(num_bookings=Count('booking')).order_by('-num_bookings')[:5]

    # Top 5 users who purchase the most bookings
    top_users = (
    Booking.objects
    .values('user') 
    .annotate(total_bookings=Count('id')) 
    .order_by('-total_bookings')[:5] 
    )
    
    user_ids = [user['user'] for user in top_users]
    users = UserProfile.objects.filter(id__in=user_ids)
    
    # Total sales for the current month
    current_month_sales = Booking.objects.filter(created_at__month=today.month, created_at__year=today.year).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Total sales for the previous month
    previous_month_sales = Booking.objects.filter(created_at__month=today.month-1, created_at__year=today.year).aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Query to get top 5 users with the most bookings
    top_users = (
        Booking.objects
        .values('user') 
        .annotate(total_bookings=Count('id'))  
        .order_by('-total_bookings')[:5]  
    )

    # Extract user IDs from the top_users query
    user_ids = [user['user'] for user in top_users]

    # Fetch all users that match the IDs in one query
    users = UserProfile.objects.filter(id__in=user_ids)

    # Create a dictionary to map user IDs to user instances
    user_dict = {user.id: user for user in users}

    # Prepare the context with user instances and their booking counts
    top_users_with_details = [
        {
            'user': user_dict[user['user']],  
            'total_bookings': user['total_bookings']  
        }
        for user in top_users
    ]

    context = {
        'bookings_last_week': bookings_last_week,
        'bookings_last_month': bookings_last_month,
        'mostly_booked_rooms': mostly_booked_rooms,
        'top_users': top_users_with_details,
        'current_month_sales': current_month_sales,
        'previous_month_sales': previous_month_sales,
    }

    return render(request, 'admin/dashboard.html', context)

@login_required(login_url="login-page")
@user_passes_test(is_admin, login_url='login-page')
def hotel_crud(request):
    hotels = Hotel.objects.all()
    return render(request,"admin/hotel_crud.html",{"hotels":hotels})

@login_required(login_url="login-page")
@user_passes_test(is_admin, login_url='login-page')
def edit_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)  
    if request.method == 'POST':
        form = HotelForm(request.POST, instance=hotel)
        if form.is_valid():
            form.save() 
            messages.success(request, f'Hotel "{hotel.name}" has been updated successfully.')
            return redirect('hotel_crud')  
    else:
        form = HotelForm(instance=hotel) 

    return render(request, 'admin/edit_hotel.html', {'form': form, 'hotel': hotel})



# Delete hotel view
@login_required(login_url="login-page")
@user_passes_test(is_admin, login_url='login-page')
def delete_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id)  
    hotel_name = hotel.name  
    
    if request.method == 'POST':
        hotel.delete() 
        messages.success(request, f'Hotel "{hotel_name}" has been deleted successfully.')
        return redirect('hotel_crud')  
    
    return render(request, 'admin/confirm_delete_hotel.html', {'hotel': hotel})



stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def payment_view(request):
    return render(request, 'hotels/payments.html', {
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY
    })

@csrf_exempt  
def create_payment(request):
    
    if request.method == 'POST':
        # Extract booking details from the request
        try:
            data = json.loads(request.body)  
            hotel_name = data.get('hotelName')
             # Retrieve the hotel price
            hotel = Hotel.objects.get(name=hotel_name)
            price_per_night = hotel.price_per_night
            payment_method_id = data.get('paymentMethodId')
            check_in_date = data.get('checkInDate')
            check_out_date = data.get('checkOutDate')
            # Calculate the number of nights
            check_in = timezone.datetime.fromisoformat(check_in_date)
            check_out = timezone.datetime.fromisoformat(check_out_date)
            number_of_nights = (check_out - check_in).days

            # Calculate the total amount
            total_amount = price_per_night * number_of_nights * 100  # Convert to cents
            total_amount_int = int(total_amount)  
            # Create a PaymentIntent with the order amount and currency
            payment_intent = stripe.PaymentIntent.create(
                amount=total_amount_int,
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                return_url='http://127.0.0.1:8000/hotel/hotel_list',  # Update this URL as needed
            )

            # Save booking information to the database
            booking = Payment.objects.create(
                user=request.user,
                amount=total_amount / 100, 
                stripe_payment_id=payment_intent.id,
                hotel_name=hotel_name,
                check_in=check_in_date,
                check_out=check_out_date
            )

            return JsonResponse({'success': True, 'paymentIntent': payment_intent})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def contact_us(request):
    
    return render(request, "hotels/contact_us.html")

def about_us(request):
    
    return render(request, "hotels/about_us.html")