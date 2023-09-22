from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Product, Lesson, UserProductAccess, LessonView
from product.serializers import ProductListSerializer, LessonListSerializer, \
    LessonDetailSerializer, ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailAPIView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = get_object_or_404(UserProductAccess, id=product_id)
        print(product.product)
        return Response(product.product)


class GetProductAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)

        lesson_ids_with_access = list(UserProductAccess.objects.filter(user=user, product=product).values_list(
            'product__product_lesson', flat=True
        ))
        print(lesson_ids_with_access)
        queryset = Lesson.objects.filter(id__in=lesson_ids_with_access)
        return queryset

    # def get_last_viewed(self, lesson):
    #     user = self.context['request'].user
    #     access = lesson.userproductaccess_set.filter(user=user).first()
    #     if access and access.last_viewed:
    #         return access.last_viewed
    #     return None

    # def get_object(self):
    #     lesson_id = self.kwargs['lesson_id']
    #     user = self.request.user
    #
    #     # Проверяем, есть ли запись UserProductAccess для данного урока и пользователя
    #     access, created = UserProductAccess.objects.get_or_create(lesson_id=lesson_id, user=user)
    #
    #     # Обновляем поле last_viewed на текущую дату и время
    #     access.last_viewed = timezone.now()
    #     access.save()
    #
    #     return Lesson.objects.get(id=lesson_id)


# class LessonDetailView(generics.RetrieveAPIView):
#     serializer_class = LessonDetailSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         lesson_id = self.kwargs['lesson_id']
#         user = self.request.user
#
#         # Получаем объект урока
#         lesson = Lesson.objects.get(id=lesson_id)
#
#         # Получаем связанный продукт
#         product = lesson.product
#
#         # Проверяем, есть ли запись UserProductAccess для данного пользователя и продукта
#         access, created = UserProductAccess.objects.get_or_create(user=user, product=product)
#
#         # Определяем время начала просмотра
#         start_time = timezone.now()
#
#         # Здесь может быть ваша логика просмотра урока
#         # Например, вы можете обновить статус просмотра урока на "В процессе"
#         lesson.status = Lesson.ViewStatusType.NOT_VIEWED
#         lesson.save()
#         # Определяем время окончания просмотра
#         end_time = timezone.now()
#
#         # Вычисляем продолжительность просмотра
#         viewing_time = end_time - start_time
#
#         # Сохраняем время просмотра в поле viewing_time
#         access.viewing_time = viewing_time
#         access.save()
#
#         return lesson
#
#     def get_last_viewed(self, lesson):
#         user = self.context['request'].user
#         access = lesson.userproductaccess_set.filter(user=user).first()
#         if access and access.last_viewed:
#             return access.last_viewed
#         return None


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        lesson_ids_with_access = UserProductAccess.objects.filter(user=user).values_list('product__product_lesson',
                                                                                         flat=True)
        queryset = Lesson.objects.filter(id__in=lesson_ids_with_access)

        return queryset

    def update_view_time(self, lesson):
        user = self.request.user
        LessonView.objects.create(user=user, lesson=lesson)

    def get_last_viewed(self, lesson):
        user = self.context['request'].user
        access = lesson.userproductaccess_set.filter(user=user).first()
        if access and access.last_viewed:
            return access.last_viewed
        return None

    def get_object(self):
        lesson_id = self.kwargs['lesson_id']
        user = self.request.user

        # Получаем объект урока
        lesson = Lesson.objects.get(id=lesson_id)

        # Получаем связанный продукт
        product = lesson.product

        # Проверяем, есть ли запись UserProductAccess для данного пользователя и продукта
        access, created = UserProductAccess.objects.get_or_create(user=user, product=product)

        # Определяем время начала просмотра
        start_time = timezone.now()

        # Здесь может быть ваша логика просмотра урока
        # Например, вы можете обновить статус просмотра урока на "В процессе"
        lesson.status = Lesson.ViewStatusType.NOT_VIEWED
        lesson.save()
        # Определяем время окончания просмотра
        end_time = timezone.now()

        # Вычисляем продолжительность просмотра
        viewing_time = end_time - start_time

        # Сохраняем время просмотра в поле viewing_time
        access.viewing_time = viewing_time
        access.save()

        return lesson

class UserProductAccessAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        access = UserProductAccess(user=user, product=product, access_date=timezone.now())
        access.save()
        return Response({'message': 'successful'}, status=status.HTTP_201_CREATED)
