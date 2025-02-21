from django.urls import path
from .views import index_view, encrypt_view, decrypt_view

urlpatterns = [
    path('', index_view, name='home'),  # Kirish sahifasi
    path('encrypt/', encrypt_view, name='encrypt_page'),  # Shifrlash sahifasi
    path('decrypt/', decrypt_view, name='decrypt_page'),  # Deshifrlash sahifasi
    
]
