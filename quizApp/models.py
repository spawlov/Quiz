from django.contrib.auth.models import User
from django.db import models


class GroupTest(models.Model):
    """Наборы тестов"""
    name = models.CharField(max_length=128, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Набор тестов'
        verbose_name_plural = 'Наборы тестов'


class Questions(models.Model):
    """Вопросы"""
    title = models.TextField(verbose_name='Вопрос')
    group = models.ForeignKey(
        GroupTest, on_delete=models.CASCADE, verbose_name='Набор тестов'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answers(models.Model):
    """Варианты ответов"""
    test = models.ForeignKey(
        Questions, on_delete=models.CASCADE, verbose_name='Тест'
    )
    text = models.TextField(verbose_name='Вариант ответа')
    correct = models.BooleanField(default=False, verbose_name='Верный ответ')

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class UserAnswers(models.Model):
    """Ответы пользователя"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    test_date = models.DateTimeField(
        auto_now=True, verbose_name='Дата прохождения'
    )
    test = models.ForeignKey(
        GroupTest, on_delete=models.DO_NOTHING, verbose_name='Тест'
    )
    quest = models.ForeignKey(
        Questions, on_delete=models.DO_NOTHING, verbose_name='Вопрос'
    )
    answers = models.CharField(max_length=128, verbose_name='Ответы')

    def __str__(self):
        return f'{self.user}, Тест: {self.test}'

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователя'
