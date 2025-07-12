"""
URL configuration for mydash project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from backenddash import views as backend_views
from myproducts import views as products_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', backend_views.signup, name='signup'),
    path('login/', backend_views.login, name='login'),
    path('view_users/', backend_views.view_users, name='view_users'),
    path('delete_user/', backend_views.delete_user, name='delete_user'),
    path('update_user/', backend_views.update_user, name='update_user'),
    path('add_product/', products_views.add_product, name='add_product'),
    path('view_products/', products_views.view_products, name='view_products'),
    path('delete_products/', products_views.delete_products, name='delete_products'),
    path('update_products/', products_views.update_products, name='update_products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
