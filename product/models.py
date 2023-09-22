from django.db import models
import cv2

from product.utils import validate_video
from users.models import CustomUser


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_author')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    class ViewStatusType(models.TextChoices):
        VIEWED = "Просмотрено"
        NOT_VIEWED = "Не просмотрено"
        IN_PROGRESS = "В прогрессе"

    title = models.CharField(max_length=255)
    video = models.FileField(upload_to="lesson/", validators=[validate_video], null=True, blank=True)
    desc = models.TextField()
    duration = models.DurationField(null=True, blank=True)
    view_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=ViewStatusType.choices, default=ViewStatusType.NOT_VIEWED)
    product = models.ManyToManyField(Product, related_name='product_lesson')

    @property
    def get_video_url(self):  # noqa
        return self.video.path

    def get_viewed_duration(self, user):
        lesson_views = LessonView.objects.filter(user=user, lesson=self)
        total_duration = sum([view.lesson.duration.total_seconds() for view in lesson_views])
        return total_duration

    def get_video_duration(self):
        try:
            cap = cv2.VideoCapture(self.get_video_url)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps
            cap.release()
            return duration
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def __str__(self):
        return self.title


class UserProductAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_product_access')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_access')
    access_date = models.DateTimeField(auto_now_add=True)
    last_viewed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "product"]


class LessonView(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"