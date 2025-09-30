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
#from django.contrib import admin
from django.urls import path
from user.views import TestUsersView
from session.views import TestLoginView, LoginView, LogoutView
from app.views.home import HomeView, HomeItemsView
from app.views.items import ItemsInfoView, ItemListView, ItemsSectionView, ItemView
from app.views.index import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name="index"),

    # Organization management app endpoints:
    # Paths with HTML GUI for users:
    #path('admin/', admin.site.urls),

    path('<str:app>/test_users/', TestUsersView.as_view(), name='test_users'),
    path('<str:app>/test_login/', TestLoginView.as_view(), name='test_login'),
    path('<str:app>/login/'     , LoginView    .as_view(), name='login'     ),
    path('<str:app>/logout/'    , LogoutView   .as_view(), name='logout'    ),
    path('<str:app>/'           , HomeView     .as_view(), name='app_home'  ),
    path('<str:app>/home_items/', HomeItemsView.as_view(), name='home_items'),

    # Paths with useful tools for application:
    path('<str:app>/items_info/' , ItemsInfoView .as_view(), name='items_info' ),
    path('<str:app>/item_list/'  , ItemListView  .as_view(), name='item_list'  ),
    path('<str:app>/items_section/', ItemsSectionView.as_view(), name='items_section'),
    path('<str:app>/item/'       , ItemView      .as_view(), name='item'       ),
]
