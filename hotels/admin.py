from django.contrib import admin
from hotels.models import Hotel, Booking, Review
from django.db.models import Count, Sum
from django.utils.timezone import now, timedelta
from users.models import UserProfile

admin.site.register(Hotel)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(UserProfile)

# class DashboardAdmin(admin.AdminSite):
#     site_header = "Hotel Booking Dashboard"

#     def get_urls(self):
#         from django.urls import path
#         urls = super().get_urls()
#         custom_urls = [
#             path('stats/', self.admin_view(self.stats_view), name='admin-stats'),
#         ]
#         return custom_urls + urls

#     def stats_view(self, request):
#         from django.shortcuts import render

#         # Bookings in last week and month
#         last_week = now() - timedelta(days=7)
#         last_month = now() - timedelta(days=30)
#         weekly_bookings = Booking.objects.filter(created_at__gte=last_week).count()
#         monthly_bookings = Booking.objects.filter(created_at__gte=last_month).count()

#         # Most booked rooms
#         top_hotels = Hotel.objects.annotate(book_count=Count('booking')).order_by('-book_count')[:5]

#         # Top 5 users who booked the most
#         top_users = Booking.objects.values('user__username').annotate(book_count=Count('id')).order_by('-book_count')[:5]

#         # Total sales
#         current_month_sales = Booking.objects.filter(created_at__month=now().month).aggregate(total=Sum('total_price'))['total'] or 0
#         previous_month_sales = Booking.objects.filter(created_at__month=(now().month - 1)).aggregate(total=Sum('total_price'))['total'] or 0

#         context = {
#             'weekly_bookings': weekly_bookings,
#             'monthly_bookings': monthly_bookings,
#             'top_hotels': top_hotels,
#             'top_users': top_users,
#             'current_month_sales': current_month_sales,
#             'previous_month_sales': previous_month_sales,
#         }
#         return render(request, 'admin/dashboard.html', context)

# admin_site = DashboardAdmin(name='dashboard')

