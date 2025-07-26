# HOST: http://127.0.0.1:8000  
#   path('', HomeView.as_view(), name='home'), 
#     path('my-account/', include("accounts.urls", namespace="accounts")),
#     path('accounts/', include("allauth.urls")),
#     path('products/', include("product.urls", namespace="product")),
#     path('order/', include("order.urls", namespace="order")),
#     path('cart/', include("cart.urls", namespace="cart")),
#     path('contact/', include("contact.urls", namespace="contact")),
#     path('admin/', admin.site.urls),
#     path('mohamed/', custom_admin_site.urls),
#     path('terms/', TermsOfServiceView.as_view(), name='terms_of_service'),
#     path("privacy/", PrivacyPolicy.as_view(), name="privacy_policy"),

# app_name = "product"

# urlpatterns = [
#     path("", ProductListView.as_view(), name="product_list"),
#     path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
# ]

# app_name = "order"

# urlpatterns = [
#     path("", OrderListView.as_view(), name="order_list"),
#     path("<uuid:pk>/", OrderDetailView.as_view(), name="order_detail"),
#     path("create/", OrderCreateView.as_view(), name="create_order"),
#     path("<uuid:pk>/cancel/", OrderCancelView.as_view(), name="cancel_order"),
#     path("addresses/", AddressListCreateView.as_view(), name="address_list_create"),
#     path("addresses/<uuid:pk>/edit/", AddressEditView.as_view(), name="address_edit"),
#     path("addresses/<uuid:pk>/delete/", AddressDeleteView.as_view(), name="address_delete"),
#     path("addresses/<uuid:pk>/set_default/", AddressSetDefaultView.as_view(), name="address_set_default"),
#     path("addresses/<uuid:pk>/unset_default/", AddressUnsetDefaultView.as_view(), name="address_unset_default"),
# ]

# app_name = "contact"

# urlpatterns = [
#     path("", SendEmailView.as_view(), name="contact"),
# ]

# app_name = "cart"
# urlpatterns = [
#     path("", CartView.as_view(), name="cart_list"),
#     path("add/<slug:slug>/", cart_add, name="cart_add"),
#     path("remove/<slug:slug>/", cart_remove, name="cart_remove"),
#     path("update/<slug:slug>/", cart_update, name="cart_update"),
#     path("clear/", cart_clear, name="cart_clear"),
# ]

# app_name = 'accounts'
# urlpatterns = [
#     path('profile/', profile_view, name='profile'),
#     path('profile/wishlist/', view_wishlist, name='wishlist'),
#     path('profile/wishlist/<slug:slug>/remove/', remove_wishlist, name='remove_wishlist'),
#     path('profile/wishlist/toggle/', toggle_wishlist, name='toggle_wishlist'),
#     path('profile/wishlist/clear/', clear_wishlist, name='clear_wishlist'),
#     path('profile/edit/', edit_profile, name='edit_profile'),
# ]
# http://127.0.0.1:8000/en/products/?search=%D9%82%D9%85%D9%8A%D8%B5&category=&tag=%D8%AE%D8%B5%D9%85&min_price=50.2300000000000&max_price=100&sort_by=name_desc&view_mode=grid&items_per_page=24
