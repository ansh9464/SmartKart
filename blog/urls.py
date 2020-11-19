"""Function views
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

admin.site.site_header = "GoCart Blog"
admin.site.site_title = "GoCart Blog Panel"
admin.site.index_title = "Welcome to GoCart admin panel"

urlpatterns = [
    path('', views.index,name="BlogHome"),
    path('blogpost/<int:id>', views.blogpost,name="Blogpost"),
    path('contactus/', views.contactus,name="contactus"),
    path('aboutus/', views.aboutus,name="about"),
    path('search/', views.search,name="search"),
    path('signup/', views.handleSignup,name="signup"),
    path('login/', views.handleLogin,name="login"),
    path('logout/', views.handleLogout,name="logout"),
]