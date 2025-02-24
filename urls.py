"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path("", include("account.urls")),
    path('admin/', admin.site.urls),
    path("dashboard/", include("dashboard.urls", namespace='dashboard')),
    path("department/", include("department.urls", namespace='department')),
    path("info/", include("info.urls", namespace='info')),
    path("invoice/", include("invoice.urls", namespace='invoice')),
    path("material_request/", include("material_request.urls", namespace='material_request')),
    path("payment/", include("payment.urls", namespace='payment')),
    path("ticket/", include("ticket.urls", namespace='ticket')),
]