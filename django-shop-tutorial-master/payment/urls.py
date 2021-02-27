from django.conf.urls import url
from django.urls import path,re_path
from . import views

urlpatterns = [
    url(r'^process/$', views.payment_process
        , name='process'),
    url(r'^done/$', views.payment_done
        , name='done'),
    url(r'^canceled/$', views.payment_canceled
        , name='canceled'),
    path("handlerequest/", views.handlerequest, name="handlerequest"),
    path('callback/', views.callback, name='callback'),
]
