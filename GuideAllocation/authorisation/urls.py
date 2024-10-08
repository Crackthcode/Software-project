"""
URL configuration for Login project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

urlpatterns = [
	path('admin/', admin.site.urls),
	# Here we are assigning the path of our url
	path('', views.signIn),
	path('postsignIn/', views.postsignIn),
	path('signUp/', views.signUp, name="signup"),
	path('logout/', views.logout, name="log"),
	path('postsignUp/', views.postsignUp),
    path('reset/', views.reset),
    path('postReset/', views.postReset),
    path('signIn/',views.signIn),
     path('postOtp/', views.postOtp, name='postOtp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('profile/', views.profile, name='profile'),
    path('emailver/', views.emailver, name='emailver'),
]


