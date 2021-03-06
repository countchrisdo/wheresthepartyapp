# Generated by Django 3.2.3 on 2021-07-22 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=500)),
                ('date', models.DateField()),
                ('hours_of_op', models.CharField(default='7:30am - 9:30pm', max_length=150)),
                ('covid_protocol', models.CharField(choices=[('Nothing Specified', 'Nothing Specified'), ('Vaccination Required', 'Vaccination Required'), ('Mask Required Indoors', 'Mask Required Indoors'), ('Vaccination and Masks Required Indoors', 'Vaccination and Masks Required Indoors')], default='Nothing Specified', max_length=50, verbose_name='Covid Protocol')),
                ('admission_fee', models.CharField(default='$5.00', max_length=100)),
                ('age_rating', models.CharField(choices=[('General Admission', 'General Admission'), ('Teens 13+', 'Teens 13+'), ('Adults 18+', 'Adults 18+'), ('Adults 21+', 'Adults 21+')], default='General Admission', max_length=50, verbose_name='Age Rating')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.event')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=280)),
                ('date', models.DateField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
