from django.urls import path
from hotels.views import (hotel_list, hotel_detail, book_hotel,hotel_crud,payment_view,
                    add_review, admin_dashboard,add_hotel,edit_hotel,delete_hotel,
                    create_payment,contact_us,about_us)


urlpatterns = [
    path('', hotel_list, name='hotel_list'),
    path('hotel/<int:hotel_id>/', hotel_detail, name='hotel_detail'),
    path('hotel/<int:hotel_id>/book/', book_hotel, name='book_hotel'),
    path('hotel/<int:hotel_id>/review/', add_review, name='add_review'),
    path('hotel/admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('hotel/add_hotel/', add_hotel, name='add_hotel'),
    path('hotel/hotel_list',hotel_list, name='hotel_list'),
    path('hotel/hotel_crud/',hotel_crud, name='hotel_crud'),
    path('hotel/edit/<int:id>/',edit_hotel, name='edit_hotel'),
    path('hotel/delete/<int:id>/',delete_hotel, name='delete_hotel'),
    path('hotel/payments/',payment_view, name='payments'),
    path('hotel/create_payment/',create_payment, name='create_payment'),
    path('hotel/contact_us/',contact_us, name='contact_us'),
    path('hotel/about_us/',about_us, name='about_us'),
]

