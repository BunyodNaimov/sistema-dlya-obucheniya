from django.urls import path

from product.views import ProductListAPIView, LessonListAPIView, UserProductAccessAPIView, GetProductAPIView, \
    ProductDetailAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('add_access/<int:product_id>/', UserProductAccessAPIView.as_view(), name='add_access'),
    path('<int:product_id>/lessons/', ProductDetailAPIView.as_view(), name='lessons'),
    path('lesson_list/', LessonListAPIView.as_view(), name='lesson_list'),
    # path('<int:product_id>/<int:lesson_id>/lesson/', LessonDetailView.as_view(), name='lesson_detail'),

]