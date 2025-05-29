from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views  
from core import views as core_views
from inediti import views as inediti_views
from scaduti import views as scaduti_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', core_views.index_view, name='index'),
    path('profilo/', core_views.profile_view, name='profilo'),  # Changed from profile_view/ to profilo/
    path('scheda_libro/<str:type>/<int:pk>/', core_views.scheda_libro, name='scheda_libro'),
    path('scheda_autore/<int:pk>/', core_views.scheda_autore, name='scheda_autore'),
    path('sign_in/', core_views.sign_in, name='sign_in'),
    path('user_login/', core_views.user_login, name='user_login'),
    path('user_logout/', core_views.user_logout, name='user_logout'),
    path('search/', core_views.search_books, name='search_books'),
    path('delete_book/<str:type>/<int:pk>/', core_views.delete_book, name='delete_book'),
    path('privacy-policy/', core_views.privacy_policy, name='privacy_policy'),
    path('add_inedito/', inediti_views.add_inedito, name='add_inedito'),
    path('add_scaduto/', scaduti_views.add_scaduto, name='add_scaduto'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)