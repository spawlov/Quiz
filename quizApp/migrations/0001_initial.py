# Generated by Django 4.1.3 on 2022-12-04 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Вопрос')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizApp.grouptest')),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Вариант ответа')),
                ('correct', models.BooleanField(default=False, verbose_name='Верный ответ')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizApp.questions', verbose_name='Тест')),
            ],
        ),
    ]
