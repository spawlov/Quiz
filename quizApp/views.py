from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from .models import GroupTest, Questions, Answers, UserAnswers


class IndexView(ListView):
    """Главная страница, список тестов"""
    model = GroupTest
    ordering = 'pk'
    template_name = 'index.html'
    context_object_name = 'groups'


class TestView(LoginRequiredMixin, ListView):
    """Прохождение теста"""
    template_name = 'quest.html'
    context_object_name = 'quest'

    def get_queryset(self):
        """Получение очередного вопроса.
        Номер вопроса передается через сессию,
        чтобы не было возможности перескочить через вопрос,
        задав его в адресной строке"""
        group = get_object_or_404(GroupTest, pk=self.kwargs.get('pk'))
        quest_lst = list(
            Questions.objects.filter(group=group).values_list('pk', flat=True)
        )
        if 'idx' not in self.request.session:
            self.request.session['idx'] = 0
        self.idx = quest_lst[self.request.session['idx']]
        queryset = get_object_or_404(Questions, pk=self.idx)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Answers.objects.filter(test=self.idx)
        # Вывод сообщения, если не выбран ни один вариант
        if self.request.session.get('Validate'):
            context['validate'] = 'Выберите вариант ответа'
        return context


@login_required
def user_answer(request):
    """Проверка и сохранение ответов пользователя"""
    if not request.POST.getlist('answer'):
        request.session['Validate'] = True
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        request.session['Validate'] = False

    if request.method == 'POST':
        current_user = User.objects.get(id=request.user.id)
        group = GroupTest.objects.get(id=request.POST.get('test'))
        quest = Questions.objects.get(id=request.POST.get('quest'))
        answer = '::'.join(request.POST.getlist('answer'))
        qs = UserAnswers.objects.create(
            user=current_user,
            test=group,
            quest=quest,
            answers=answer
        )
        qs.save()
        count = Questions.objects.filter(
            group_id=request.POST.get('test')
        ).count()
        if request.session['idx'] + 1 < count:
            request.session['idx'] += 1
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            del request.session['idx']
            return redirect(f'/result/{request.POST.get("test")}/')
    else:
        return HttpResponse('<h1>Wrong method</h1>')


class UserResult(LoginRequiredMixin, ListView):
    """Результат прохождения теста"""
    model = UserAnswers
    template_name = 'result.html'
    context_object_name = 'results'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Формирования списка верных/неверных ответов
        test = self.kwargs.get('group')
        quest = Questions.objects.filter(
            group_id=test
        ).values_list('id', flat=True)
        context_dict = {}
        for i in quest:
            answer = Answers.objects.filter(test_id=i).values(
                'pk', 'test__title', 'text', 'correct'
            )
            user = UserAnswers.objects.filter(
                quest_id=i, user=self.request.user
            ).latest('test_date')
            answer_list = list(map(int, user.answers.split('::')))
            val_dict = {}
            for d in answer:
                if all([d['pk'] in answer_list, d['correct']]):
                    val_dict[d['pk']] = d['text'], True
                    context_dict[i] = d['test__title'], val_dict
                elif all([d['pk'] in answer_list, not d['correct']]):
                    val_dict[d['pk']] = d['text'], False
                    context_dict[i] = d['test__title'], val_dict
                elif all([d['pk'] not in answer_list, d['correct']]):
                    val_dict[d['pk']] = d['text'], True
                    context_dict[i] = d['test__title'], val_dict
                else:
                    val_dict[d['pk']] = d['text'], True
                    context_dict[i] = d['test__title'], val_dict
        context['answers'] = context_dict

        # Количество и процент верных ответов
        context['count_question'] = quest.count()
        count_correct = 0
        for _, val in context_dict.values():
            ans_lst = []
            for __, var in val.values():
                ans_lst.append(var)
            if all(ans_lst):
                count_correct += 1
        context['count_correct'] = count_correct
        context['correct_percent'] = round(
            count_correct * 100 / quest.count(), 2
        )

        return context
