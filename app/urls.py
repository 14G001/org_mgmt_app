"""
URL configuration for app project.

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
from session.views import LoginView, LogoutView
from org_mgmt_app.views.home import AppHomeView, HomeItemsView
from org_mgmt_app.views.items import ItemsInfoView, ItemListView, ItemsSectionView, CreateItemView, ItemView, UpdateItemView, DeleteItemView
from app.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name="home"),

    # Organization management app endpoints:
    # Paths with HTML GUI for users:
    #path('admin/', admin.site.urls),
    path('<str:app>/login/' , LoginView  .as_view(), name='login'),
    path('<str:app>/logout/', LogoutView .as_view(), name='logout'),
    path('<str:app>/'       , AppHomeView.as_view(), name='app_home'),
    path('<str:app>/home_items/', HomeItemsView.as_view(), name='home_items'),

    # Paths with useful tools for application:
    path('<str:app>/items_info/' , ItemsInfoView .as_view(), name='items_info' ),
    path('<str:app>/item_list/'  , ItemListView  .as_view(), name='item_list'  ),
    path('<str:app>/items_section/', ItemsSectionView.as_view(), name='items_section'),
    path('<str:app>/new_item/'   , CreateItemView.as_view(), name='new_item'   ),
    path('<str:app>/item_fields/', ItemView      .as_view(), name='item_fields'),
    path('<str:app>/update_item/', UpdateItemView.as_view(), name='udpate_item'),
    path('<str:app>/delete_item/', DeleteItemView.as_view(), name='delete_item'),
]
