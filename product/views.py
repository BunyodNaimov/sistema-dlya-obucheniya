from django.db import IntegrityError
from django.db.models import Count, Sum, F
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product.models import Product, Lesson, UserProductAccess, LessonView
from product.serializers import ProductListSerializer, LessonListSerializer, \
    UserProductAccessAPIViewSerializer, ProductStatsSerializer


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        lesson_ids_with_access = UserProductAccess.objects.filter(user=user).values_list('product__product_lesson',
                                                                                         flat=True)
        queryset = Lesson.objects.filter(id__in=lesson_ids_with_access)

        for lesson in queryset:
            try:
                lesson_view = LessonView.objects.get(user=user, lesson=lesson)
                lesson.viewed = True
                lesson.view_time = lesson_view.view_time
            except LessonView.DoesNotExist:
                lesson.viewed = False
                lesson.view_time = None

        return queryset

    def update_view_time(self, lesson):
        user = self.request.user
        lesson.viewed = True
        lesson.view_time = timezone.now()
        lesson.save()
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

        # Обновляем статус урока на "В процессе" (если требуется)
        if lesson.status != Lesson.ViewStatusType.VIEWED:
            lesson.status = Lesson.ViewStatusType.IN_PROGRESS
            lesson.save()

        # Обновляем время последнего просмотра
        access.last_viewed = timezone.now()
        access.save()

        return lesson


class UserProductAccessAPIView(generics.GenericAPIView):
    serializer_class = UserProductAccessAPIViewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        try:
            access = UserProductAccess.objects.create(user=user, product=product, access_date=timezone.now())
            access.save()
            return Response({'message': 'successful'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'message': 'Product already added'}, status=status.HTTP_400_BAD_REQUEST)


class ProductLessonListAPIView(generics.ListAPIView):
    serializer_class = LessonListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']

        # Получаем доступы пользователя к продуктам
        user_product_accesses = UserProductAccess.objects.filter(user=user, product_id=product_id)

        # Получаем уроки, связанные с данным продуктом и доступными пользователю
        lesson_ids_with_access = user_product_accesses.values_list('product__product_lesson', flat=True)
        queryset = Lesson.objects.filter(id__in=lesson_ids_with_access)

        # Добавляем информацию о статусе просмотра, времени просмотра и дате последнего просмотра ролика
        for lesson in queryset:
            try:
                lesson_view = LessonView.objects.get(user=user, lesson=lesson)
                lesson.viewed = True
                lesson.view_time = lesson_view.view_time
                lesson.last_viewed = lesson_view.last_viewed
            except LessonView.DoesNotExist:
                lesson.viewed = False
                lesson.view_time = None
                lesson.last_viewed = None

        return queryset


class ProductStatsAPIView(generics.ListAPIView):
    serializer_class = ProductStatsSerializer

    def get_queryset(self):
        queryset = Product.objects.annotate(
            total_lessons_viewed=Count('product_lesson__lessonview'),
            total_view_duration=Sum('product_lesson__lessonview__lesson__duration'),
            total_students=Count('product_access__user', distinct=True),
            percent_purchased=(Count('product_access__user', distinct=True) * 100) / F('author__total_users'),
        ).values('id', 'name', 'total_lessons_viewed', 'total_view_duration', 'total_students', 'percent_purchased')

        return queryset
