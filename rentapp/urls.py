from django.urls import path
from . import views

app_name = 'rentapp'

urlpatterns = [
    # Páginas principales
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

    # Mensajería
    path('conversaciones/', views.conversaciones_list, name='conversaciones'),
    path('chat/<int:conversacion_id>/', views.chat_view, name='chat'),
    path('iniciar-conversacion/<int:local_id>/', views.iniciar_conversacion, name='iniciar_conversacion'),
    path('chat/<int:conversacion_id>/poll/', views.obtener_mensajes_nuevos, name='obtener_mensajes_nuevos'),
    path('api/mensajes/no-leidos/', views.contar_mensajes_no_leidos, name='contar_mensajes_no_leidos'),
    path('api/conversaciones/', views.api_conversaciones, name='api_conversaciones'),
]