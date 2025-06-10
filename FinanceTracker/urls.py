from django.contrib import admin
from django.urls import path,include,re_path
#path() is used for clean, readable URLs
#include() is used to connect to other apps’ URL files
#re_path() lets you use regular expressions
from django.views.generic.base import RedirectView

fav_icon = RedirectView.as_view(url='/static/icons/favicons.ico', permanent=True)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/', include('userexpense.urls')),
    path('', include('dashboard.urls')),
    path('auth/', include('allauth.urls')),
    path('income/', include('userincome.urls')),
    path('preferences/', include('userprefer.urls')),
    re_path(r'^favicon\.ico$', fav_icon),
]
