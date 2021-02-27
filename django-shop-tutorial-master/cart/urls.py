from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^&#8377;', views.cart_detail,
        name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/&#8377;',
        views.cart_add,
        name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/&#8377;',
        views.cart_remove,
        name='cart_remove'),
]
