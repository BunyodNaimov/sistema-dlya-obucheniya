from rest_framework import serializers

from product.models import Product, Lesson, UserProductAccess, LessonView


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserProductAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductAccess
        fields = ['user', 'product', 'access_date', 'last_viewed']


class LessonListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    def get_product(self, lesson):
        product = lesson.product.first()
        if product:
            return ProductSerializer(product).data
        return None

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'desc', 'product', 'get_video_url', 'get_video_duration', 'status',
                  'last_viewed', 'view_time')


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductAccess
        fields = ('id', 'product_id')


class ProductListSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'author', 'lessons')


class UserProductAccessAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductAccess
        fields = ('id', 'product_id')


class ProductStatsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    total_lessons_viewed = serializers.IntegerField()
    total_view_duration = serializers.DurationField()
    total_students = serializers.IntegerField()
    percent_purchased = serializers.FloatField()
