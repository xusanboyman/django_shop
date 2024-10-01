from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('delete_product/<str:pk>/', views.deleteProduct, name="delete_product"),
    path('edit_user/<str:user_id>/', views.edit_user, name="edit_user"),
    path('', views.home, name='home'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('sellers/', views.sellers, name='sellers'),
    path('all_users/', views.all_users, name='all_users'),
    path('sellerPage/<str:pk>/', views.sellerPage, name='sellerPage'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist_delete/<int:product_id>/', views.wishlist_delete, name='wishlist_delete'),
    path('login/', views.LoginPage, name='login'),
    path('product_page/<str:pk>/', views.productRoom, name="product"),
    path('create_product/', views.create_product, name="create_product"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



