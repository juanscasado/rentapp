from django.urls import path
from . import views

app_name = 'rentapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:local_id>', views.detail, name='detail'),
    path('buscar/', views.buscar, name='buscar'),

    # Locales y fotos
    path('insertar_local/', views.insertar_local, name='insertar_local'),
    path('insertar_foto/<int:local_id>/', views.insertar_foto, name='insertar_foto'),
    path('obtener_fotos/<int:local_id>/', views.obtener_fotos, name='obtener_fotos'),
    path('foto/eliminar/<int:foto_id>/', views.eliminar_foto, name='eliminar_foto'),

    # Dashboard y delete
    path('dashboard/<int:id_user>', views.dashboard, name='dashboard'),
    path('delete_local/<int:id_local>-<int:user>', views.delete_local, name='delete_local'),
]