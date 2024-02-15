"""monitoring URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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




from django.contrib import admin
from django.urls import path, include

workers_table_patterns = [
    path("", workers_table.signin),
    path("employee", workers_table.employee_page),
    path("logout", workers_table.logout),
    path("list", workers_table.workers),
    path("register", workers_table.register),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(workers_table_patterns))
]


"""

from django.contrib import admin
from django.urls import path, include

from workers_table.views import (
    employee_page,
    logout,
    signin,
    workers,
    register,
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path("list/", workers, name='list'),
    path('register/', register, name='register'),
    path('api/', include('workers_table.urls')),
    path('', signin, name='login'),
    path('logout/', logout, name='logout'),
    path('employee/', employee_page, name='get_employee'),

]
