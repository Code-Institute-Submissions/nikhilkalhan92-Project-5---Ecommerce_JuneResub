from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('item/<str:category>', views.products_category, name='products_category'),
    path('<int:product_id>', views.product_detail, name='product_detail'),

    path('update/<int:pk>/',views.update_comment,name='update_comment'),

    path('delete/<int:pk>/',views.delete_comment,name='delete_comment'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product')
    
]