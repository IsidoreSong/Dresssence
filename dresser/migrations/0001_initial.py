# Generated by Django 3.1.5 on 2021-02-21 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ColorFirst',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ColorSecond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('color_first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dresser.colorfirst')),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StyleFeeling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happy', models.FloatField()),
                ('sad', models.FloatField()),
                ('style', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dresser.style')),
            ],
        ),
        migrations.CreateModel(
            name='StyleCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening', models.FloatField()),
                ('outgoing', models.FloatField()),
                ('style', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dresser.style')),
            ],
        ),
        migrations.CreateModel(
            name='ColorThird',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('common_name', models.CharField(max_length=20)),
                ('color_second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dresser.colorsecond')),
            ],
        ),
        migrations.CreateModel(
            name='ColorParing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red', models.FloatField()),
                ('yellow', models.FloatField()),
                ('color', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dresser.colorthird')),
            ],
        ),
        migrations.CreateModel(
            name='ColorFeeling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happy', models.FloatField()),
                ('sad', models.FloatField()),
                ('color', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dresser.colorthird')),
            ],
        ),
        migrations.CreateModel(
            name='ColorCharacter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening', models.FloatField()),
                ('outgoing', models.FloatField()),
                ('color', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dresser.colorthird')),
            ],
        ),
    ]
