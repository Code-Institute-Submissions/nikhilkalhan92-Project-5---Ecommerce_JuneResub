from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('item/<str:category>', views.products_category, name='products_category'),
    path('<int:product_id>', views.product_detail, name='product_detail'),
<<<<<<< HEAD
=======
    path('update/<int:pk>/',views.update,name='update'),
    path('delete/<int:pk>/',views.delete,name='delete'),
>>>>>>> 5f235c82eb3bbc9acf23df9be62d57ee0173a516
]