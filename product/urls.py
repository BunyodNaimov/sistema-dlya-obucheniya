from django.urls import path

from product.views import ProductListAPIView, LessonListAPIView, UserProductAccessAPIView, \
    ProductLessonListAPIView, ProductStatsAPIView

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('<int:product_id>/lessons/', ProductLessonListAPIView.as_view(), name='product-lessons_list'),
    path('lesson_list/', LessonListAPIView.as_view(), name='lesson_list'),
    path('<int:product_id>/add_access/', UserProductAccessAPIView.as_view(), name='add_access'),
    path('stats', ProductStatsAPIView.as_view(), name='product-stats')

]
