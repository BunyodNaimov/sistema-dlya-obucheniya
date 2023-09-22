from rest_framework import serializers

from product.models import Product, Lesson, UserProductAccess, LessonView


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'author')


class LessonListSerializer(serializers.ModelSerializer):
    viewed_duration = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'desc', 'product', 'get_video_url', 'get_video_duration', 'viewed_duration', 'status')

    def get_viewed_duration(self, lesson):
        user = self.context['request'].user
        lesson_views = LessonView.objects.filter(user=user, lesson=lesson)
        total_duration = sum([view.lesson.duration.total_seconds() for view in lesson_views])
        return total_duration


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductAccess
        fields = ('id', 'product_id')


class ProductSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = UserProductAccess
        fields = ('id', 'product')
