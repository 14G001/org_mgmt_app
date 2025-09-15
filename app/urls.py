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
from organization.views.home import HomeView, HomeItemsView
from organization.views.items import ItemsInfoView, ItemListView, ItemsSectionView, CreateItemView, ItemView, UpdateItemView, DeleteItemView

urlpatterns = [
    # Paths with HTML GUI for users:
    #path('admin/', admin.site.urls),
    path('login/' , LoginView .as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(''       , HomeView  .as_view(), name='home'),
    path('home_items/', HomeItemsView.as_view(), name='home_items'),

    # Paths with useful tools for application:
    path('items_info/' , ItemsInfoView .as_view(), name='items_info' ),
    path('item_list/'  , ItemListView  .as_view(), name='item_list'  ),
    path('items_section/', ItemsSectionView.as_view(), name='items_section'),
    path('new_item/'   , CreateItemView.as_view(), name='new_item'   ),
    path('item_fields/', ItemView      .as_view(), name='item_fields'),
    path('update_item/', UpdateItemView.as_view(), name='udpate_item'),
    path('delete_item/', DeleteItemView.as_view(), name='delete_item'),
]
