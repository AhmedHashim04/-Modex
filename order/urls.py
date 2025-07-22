from django.urls import path

from .views import (OrderCancelView, OrderCreateView, OrderDetailView,
                    OrderListView, AddressListCreateView,
                    AddressEditView, AddressDeleteView, AddressSetDefaultView, AddressUnsetDefaultView)

app_name = "order"

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("<uuid:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("create/", OrderCreateView.as_view(), name="create_order"),
    path("<uuid:pk>/cancel/", OrderCancelView.as_view(), name="cancel_order"),
    path("addresses/", AddressListCreateView.as_view(), name="address_list_create"),
    path("addresses/<int:pk>/edit/", AddressEditView.as_view(), name="address_edit"),
    path("addresses/<int:pk>/delete/", AddressDeleteView.as_view(), name="address_delete"),
    path("addresses/<int:pk>/set_default/", AddressSetDefaultView.as_view(), name="address_set_default"),
    path("addresses/<int:pk>/unset_default/", AddressUnsetDefaultView.as_view(), name="address_unset_default"),
]
