# Generated by Django 4.2.5 on 2023-09-22 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproductaccess',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_product_access', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lessonview',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.lesson'),
        ),
        migrations.AddField(
            model_name='lessonview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lesson',
            name='product',
            field=models.ManyToManyField(related_name='product_lesson', to='product.product'),
        ),
        migrations.AlterUniqueTogether(
            name='userproductaccess',
            unique_together={('user', 'product')},
        ),
    ]
