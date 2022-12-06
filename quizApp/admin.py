from django.contrib import admin

from .models import Questions, GroupTest, Answers, UserAnswers


class AnswerInLine(admin.TabularInline):
    model = Answers
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    model = Questions
    ordering = ['id']
    list_display = ('group', 'title',)
    list_display_links = ('title',)
    list_filter = ('group',)
    fieldsets = [
        ('Набор тестов', {'fields': ('group',)}),
        ('Вопрос', {'fields': ('title',)}),
    ]
    inlines = (AnswerInLine,)


class AdminUserAnswers(admin.ModelAdmin):
    model = UserAnswers
    list_display = ('test_date', 'user', 'test', 'quest',)


admin.site.register(GroupTest)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(UserAnswers, AdminUserAnswers)
