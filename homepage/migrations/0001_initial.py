# Generated by Django 2.1.5 on 2019-07-29 22:09

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
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=7)),
                ('description', models.CharField(max_length=300)),
                ('image', models.FileField(upload_to='')),
                ('borrowed', models.BooleanField(default=False)),
                ('owner', models.CharField(default='', max_length=50)),
                ('category', models.CharField(choices=[('Art', 'Art'), ('Drama', 'Drama'), ('Engineering', 'Engineering'), ('Fashion', 'Fashion'), ('Food', 'Food'), ('Health', 'Health'), ('Romance', 'Romance'), ('Science', 'Science'), ('Sports', 'Sports'), ('Other', 'Other')], default='Other', max_length=15)),
                ('tags', models.CharField(blank=True, max_length=100)),
                ('donator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReturnList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Items')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=200)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=10.0, max_digits=7)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Items')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='usercart',
            unique_together={('username', 'item')},
        ),
        migrations.AlterUniqueTogether(
            name='userbalance',
            unique_together={('username', 'balance')},
        ),
        migrations.AlterUniqueTogether(
            name='returnlist',
            unique_together={('username', 'item')},
        ),
    ]