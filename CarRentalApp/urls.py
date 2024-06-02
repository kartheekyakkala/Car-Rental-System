from django.urls import path
from CarRentalApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.login,name='login'),
    path('home/',views.Home,name='home'),
    path('login/',views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    #contact
    path('contact/',views.contact,name='contact'),
    path('contact_list/',views.contact_list,name='contact_list'),
    #customerlogin,customer_register
    path('login_success/',views.login_success,name='login_success'),
    path('customer_register/',views.customer_register,name='customer_register'),
    #dashboard
    path('dashboard/',views.dashboard,name='dashboard'),
    #car_list,add_car,car_details,car,booking_car,booking,delete_booking,edit_car,delete_car
    path('booking/',views.booking,name='booking'),
    path('car/',views.car,name='car'),
    path('car_list/',views.car_list,name='car_list'),
    path('add_car/',views.add_car,name='add_car'),
    path('edit_car/<int:id>/',views.edit_car,name='edit_car'),
    path('delete_car/<int:id>/',views.delete_car,name='delete_car'),
    path('car_detail/<int:id>/',views.car_detail,name='car_detail'),
    path('total_booking/',views.total_booking,name='total_booking'),
    path('edit_booking/<int:id>/',views.edit_booking,name='edit_booking'),
    path('journey_status/<int:id>/',views.journey_status,name='journey_status'),
    path('delete_booking/<int:id>/',views.delete_booking,name='delete_booking'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)