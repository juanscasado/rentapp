from django.urls import path
from . import views

app_name = 'rentapp'
urlpatterns = [
    # register
    path('register/', views.register, name='register'),
    # insertar User
    path('insertar_user/', views.insertar_user, name='insertar_user' ),
    # prueba url
    path('prueba/', views.prueba, name='prueba'),
    # ex: /rentapp/
    path('', views.index, name='index'),
    # ex: /rentapp/2/
    path('<int:local_id>', views.detail, name='detail'),
    # ex: /rentapp/"direccion"/
    path('buscar/', views.buscar, name='buscar'),
    # ex: /rentapp/insertar_renta/
    path('insertar_local/', views.insertar_local, name='insertar_local'),
    # ex: /rentapp/insertar_foto/
    path('insertar_foto/<int:local_id>', views.insertar_foto, name='insertar_foto'),

    # ex: /rentapp/dashboard usertario
    path('dashboard/<int:id_user>', views.dashboard, name='dashboard'),
    # ex: /rentapp/dashboard userdador
   
    path('delete_local/<int:id_local>-<int:user>', views.delete_local, name='delete_local' ),
    # logout_user
    path(' ', views.logout_user, name='logout_user'),
    # login
    # path(' ', views.login_user, name='login_user'),

    # Nothing yet!
    # path('image_rentapp/', views.image_rentapp, name='image_rentapp'),
    # path('upload_image/', views.upload_image, name='upload_image'),

]