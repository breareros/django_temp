import datetime
# import sys
from datetime import date, timedelta, datetime

from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect, request
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from . import base
from .forms import AddApostilForm, EditApostilForm, AddApostilWithDateForm, GenerateChunkForm
from .models import ApostilList, Chunk
from .services import generate_chunks


# Create your views here.
def index(request):
    return render(request, 'apostil/index.html')


class AllApostil(ListView):
    model = ApostilList
    template_name = 'apostil/apostil_list.html'
    context_object_name = 'all_apostil'

    def get_queryset(self):
        apostils = ApostilList.objects.select_related('chunk')
        return apostils

class AddApostil(CreateView):
    model = ApostilList
    form_class = AddApostilForm
    template_name = 'apostil/apostil_add.html'
    success_url = reverse_lazy('chunk_list')


class AddApostilWithDate(AddApostil):
    form_class = AddApostilWithDateForm
    template_name = 'apostil/apostil_add.html'
    def form_valid(self, form):
        form.instance.chunk = Chunk.objects.get(pk=self.kwargs['id_chunk'])
        return super().form_valid(form)


class EditApostil(UpdateView):
    model = ApostilList
    form_class = EditApostilForm
    template_name = 'apostil/apostil_update.html'
    success_url = reverse_lazy('chunk_list')


class ListChunk(ListView):
    model = Chunk
    template_name = 'apostil/chunk_list.html'
    context_object_name = 'all_chunks'

    def __init__(self):
        super(ListChunk, self).__init__()
        self.limit_days = base.limit_days
        self.today = date.today()
        self.end_show_date = self.today + timedelta(days=self.limit_days)
        self.chunks = Chunk.objects.filter(date__range=(self.today, self.end_show_date),
                                           apostils__isnull=True).prefetch_related(
            'apostils').select_related('apostils__chunk')
        self.count_free_chunk_in_perid = self.chunks.count()

        print(
            f"-- init: s_day: {self.today} days: {self.limit_days} e_day: {self.end_show_date} count: {self.count_free_chunk_in_perid}")

    def get_queryset(self):
        # TODO: А если все limit_days заняты? ТО проблема да...
        # Как выбрать Chunks которые НЕ связаны с ApostilList...
        # ответ: Chunk.objects.filter(date__range=(self.today, self.end_show_date), apostils__isnull=True)

        print(f"{self.count_free_chunk_in_perid=}")
        # if self.count_free_chunk_in_period <= 8:
        while self.count_free_chunk_in_perid <= len(base.time_intervals):
            self.limit_days += 1
            self.end_show_date = self.today + timedelta(days=self.limit_days)
            print(f"{self.end_show_date=} {self.limit_days=}")
            print()
            self.count_free_chunk_in_perid = Chunk.objects.filter(date__range=(self.today, self.end_show_date),
                                                                  apostils__isnull=True).prefetch_related(
                'apostils').select_related('apostils__chunk').count()

        chunks = Chunk.objects.filter(date__range=(self.today, self.end_show_date)).prefetch_related(
            'apostils').select_related('apostils__chunk')

        return chunks

    def get_context_data(self, **kwargs):
        context = super(ListChunk, self).get_context_data(**kwargs)
        context['today'] = Chunk.objects.filter(date=self.today).prefetch_related('apostils').select_related(
            'apostils__chunk')
        context['lost'] = Chunk.objects.filter(date__lt=self.today, apostils__is_done=False,
                                               apostils__is_gone=False).prefetch_related('apostils').select_related(
            'apostils__chunk')
        context['days_count'] = Chunk.objects.filter(date=self.today).aggregate(docs=Sum('apostils__count_docs'))
        context['to_day'] = self.today

        return context



class ListChunk2(ListView):
    model = Chunk
    template_name = 'apostil/chunk_list_2.html'
    context_object_name = 'all_chunks'

    def __init__(self):
        super(ListChunk2, self).__init__()
        self.limit_days = base.limit_days
        self.today = date.today()
        self.end_show_date = self.today + timedelta(days=self.limit_days)
        self.chunks = Chunk.objects.filter(date__range=(self.today, self.end_show_date),
                                           apostils__isnull=True).prefetch_related(
            'apostils').select_related('apostils__chunk')
        self.count_free_chunk_in_period = self.chunks.count()
        self.days = self.chunks.order_by('date').values('date').distinct()
        print(f"{self.days=}")
        # print(
        #     f"-- init: s_day: {self.today} days: {self.limit_days} e_day: {self.end_show_date} count: {self.count_free_chunk_in_period}")

    def get_queryset(self):
        # TODO: А если все limit_days заняты? ТО проблема да...
        # Как выбрать Chunks которые НЕ связаны с ApostilList...
        # ответ: Chunk.objects.filter(date__range=(self.today, self.end_show_date), apostils__isnull=True)

        print(f"{self.count_free_chunk_in_period=}")
        # if self.count_free_chunk_in_period <= 8:
        while self.count_free_chunk_in_period <= len(base.time_intervals):
            self.limit_days += 1
            self.end_show_date = self.today + timedelta(days=self.limit_days)
            print(f"{self.end_show_date=} {self.limit_days=}")
            print()
            self.count_free_chunk_in_period = Chunk.objects.filter(date__range=(self.today, self.end_show_date),
                                                                   apostils__isnull=True).prefetch_related(
                'apostils').select_related('apostils__chunk').count()

        chunks = Chunk.objects.filter(date__range=(self.today, self.end_show_date)).prefetch_related(
            'apostils').select_related('apostils__chunk')

        return chunks


    def get_context_data(self, **kwargs):
        context = super(ListChunk2, self).get_context_data(**kwargs)
        context['today'] = Chunk.objects.filter(date=self.today).prefetch_related('apostils').select_related(
            'apostils__chunk')
        context['lost'] = Chunk.objects.filter(date__lt=self.today,
                                               apostils__is_done=False,
                                               apostils__is_gone=False
                                               ).prefetch_related('apostils').select_related('apostils__chunk')
        context['days_count'] = Chunk.objects.filter(date=self.today).aggregate(docs=Sum('apostils__count_docs'))
        context['to_day'] = self.today
        context['days'] = self.days
        context['per_days'] = dict()
        for d in self.days:
            print(str(d.get('date')))

            qs = Chunk.objects.filter(date=d.get('date')).prefetch_related('apostils').select_related('apostils__chunk')

            # pd = {f"{d.get('date')}": qs, 'count_day': qs.aggregate(docs=Sum('apostils__count_docs'))}
            # pd = {f"{d.get('date')}" : {'chunks': qs, 'count_docs': qs.aggregate(docs=Sum('apostils__count_docs'))}}
            pd = {f"{d.get('date')}" : {'chunks': qs, 'count_docs': qs.aggregate(docs=Sum('apostils__count_docs'))}}
            context['per_days'].update(pd)

        print(f"{context['per_days']=}")
        return context




class ListAllChunk(ListView):
    '''НЕДОДЕЛКА'''
    model = Chunk
    template_name = 'apostil/chunk_list_all.html'
    context_object_name = 'all_chunks'
    success_url = reverse_lazy('chunk_list_all')

    def get_queryset(self):
        # return Chunk.objects.filter(Q(pk__in=[b.get('chunk_id') for b in ApostilList.objects.all().values('chunk_id')]))
        # return Chunk.objects.values('id', 'date', 'time', 'chunks__fio', 'chunks__is_done', 'chunks__is_gone',
        #                             'chunks__id')  # filter(Q(pk__in=[b.get('chunk_id') for b in ApostilList.objects.all().values('chunk_id')]))
        return Chunk.objects.all().prefetch_related('apostils').select_related('apostils__chunk')
        # return Chunk.objects.values('id', 'date', 'time', 'apostils__fio', 'apostils__is_done', 'apostils__is_gone','apostils__id')  # filter(Q(pk__in=[b.get('chunk_id') for b in ApostilList.objects.all().values('chunk_id')]))


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListAllChunk, self).get_context_data(**kwargs)
        context['list_dates'] = Chunk.objects.order_by().values_list('date', flat=True).distinct()
        # print(f"{context=}")
        # print(f"{context['list_dates']=}")
        # print()
        # for c in context.items():
        #     print(f"{c=}")
        return context


def gen_chunks(request):
    '''Проверка корректности что дата начала раньше, чем дата конца в форме'''
    if request.method == 'POST':
        form = GenerateChunkForm(request.POST)

        if form.is_valid():
            generate_chunks(start_date=form.cleaned_data.get('start'), end_date=form.cleaned_data.get('end'))
            return redirect('chunk_list')
    else:
        form = GenerateChunkForm()

    return render(request, 'apostil/chunk_generate.html', {'form': form})


def report(request):
    return render(request, 'apostil/report.html')

# Вынести эту функцию в services
# def generate_chunks(start_date: date, end_date: date,
#                     time_intervals: list = base.time_intervals) -> None:
#     delta = end_date - start_date
#     print(f"{delta}, {type(delta)}: {type(start_date)} {type(end_date)}")
#     chunks_to_create = []
#     for i in range((end_date - start_date).days + 1):
#         current_date = start_date + timedelta(days=i)
#         if current_date.isoweekday() not in (6, 7):  # 6 - суббота, 7 - воскресение
#             chunks_to_create += [Chunk(date=current_date, time=datetime.strptime(t, '%H:%M').time()) for t in
#                                  time_intervals]
#
#     # Получаем список уже существующих чанков в периоде start_date - end_date
#     existing_chunks = Chunk.objects.filter(date__range=(start_date, end_date))
#
#     # Отфильтровываем из списка чанков те, которые уже были созданы ранее
#     chunks_to_create = [chunk for chunk in chunks_to_create if
#                         not existing_chunks.filter(date=chunk.date, time=chunk.time).exists()]
#
#     # Создаем новые чанки в базе данных
#     if chunks_to_create:
#         print(chunks_to_create)
#         Chunk.objects.bulk_create(chunks_to_create)

