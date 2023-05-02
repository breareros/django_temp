from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta, MO, FR

# from reportlab.pdfgen import canvas

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponse

from . import base
from .forms import AddApostilForm, EditApostilForm, AddApostilWithDateForm, GenerateChunkForm
from .models import ApostilList, Chunk
from .services import generate_chunks


def index(request):
    ''' Наверное надо на авторизацию переделать'''
    return render(request, 'apostil/index.html')


class AllApostil(ListView):
    ''' Список всех записей. всех-всех.'''
    model = ApostilList
    template_name = 'apostil/apostil_list.html'
    context_object_name = 'all_apostil'

    def get_queryset(self):
        apostils = ApostilList.objects.select_related('chunk')
        return apostils


class AddApostil(CreateView):
    '''
    Добавление записи где все можно выбрать
    '''
    model = ApostilList
    form_class = AddApostilForm
    template_name = 'apostil/apostil_add.html'
    success_url = reverse_lazy('chunk_list')


class AddApostilWithDate(AddApostil):
    '''
    Добавление записи на выбранный чанк. В самой форме выбрать чанк нельзя.
    '''
    form_class = AddApostilWithDateForm
    template_name = 'apostil/apostil_add.html'

    def form_valid(self, form):
        form.instance.chunk = Chunk.objects.get(pk=self.kwargs['id_chunk'])
        return super().form_valid(form)


class EditApostil(UpdateView):
    ''' Редактирование записи'''
    model = ApostilList
    form_class = EditApostilForm
    template_name = 'apostil/apostil_update.html'
    success_url = reverse_lazy('chunk_list')


class ListChunk(ListView):
    """ Типа deprecated используй ListChunk2"""
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
        # Ответ: Chunk.objects.filter(date__range=(self.today, self.end_show_date), apostils__isnull=True)

        print(f"{self.count_free_chunk_in_perid=}")
        # Если количество свободных чанков меньше чем количество интервалов в день (из расписания), то открываем для отображения еще день
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
        self.chunks = Chunk.objects.filter(date__range=(self.today + timedelta(days=1), self.end_show_date),
                                           apostils__isnull=True).prefetch_related(
            'apostils').select_related('apostils__chunk')
        self.count_free_chunk_in_period = self.chunks.count()
        self.days = self.chunks.order_by('date').values('date').distinct()
        # print(f"{self.days=}")

    def get_queryset(self):
        # TODO: А если все limit_days заняты? ТО ...
        # Как выбрать Chunks которые НЕ связаны с ApostilList...
        # ответ: Chunk.objects.filter(date__range=(self.today, self.end_show_date), apostils__isnull=True)

        # print(f"{self.count_free_chunk_in_period=}")
        while self.count_free_chunk_in_period <= len(base.time_intervals):
            self.limit_days += 1
            self.end_show_date = self.today + timedelta(days=self.limit_days)
            # print(f"{self.end_show_date=} {self.limit_days=}")
            # print()
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
        context['last_chunk'] = Chunk.objects.order_by('date').values('date').distinct().last()
        for d in self.days:
            # print(str(d.get('date')))
            qs = Chunk.objects.filter(date=d.get('date')).prefetch_related('apostils').select_related('apostils__chunk')
            pd = {f"{d.get('date')}": {'chunks': qs, 'count_docs': qs.aggregate(docs=Sum('apostils__count_docs'))}}
            context['per_days'].update(pd)

        # print(f"{context['per_days']=}")
        return context


class ListAllChunk(ListView):
    '''НЕДОДЕЛКА'''
    model = Chunk
    template_name = 'apostil/chunk_list_all.html'
    context_object_name = 'all_chunks'
    success_url = reverse_lazy('chunk_list_all')

    def get_queryset(self):
        return Chunk.objects.all().prefetch_related('apostils').select_related('apostils__chunk').order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListAllChunk, self).get_context_data(**kwargs)
        context['list_dates'] = Chunk.objects.order_by().values_list('date', flat=True).distinct()
        return context

class ListChunkOhrana(ListView):
    model = Chunk
    template_name = 'apostil/ohrana.html'
    context_object_name = 'today'
    def get_queryset(self):
        today = date.today()
        qs = Chunk.objects.filter(date=today).prefetch_related('apostils').select_related('apostils__chunk')
        return qs


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
    if request.method == 'POST':
        form = GenerateChunkForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data.get('start')
            stop_date = form.cleaned_data.get('end')
            print(f"{start_date=}")
            print(f"{stop_date=}")
            # ch = Chunk.objects.filter(date__range=(start_date, stop_date), apostils__isnull=False).prefetch_related('apostils').select_related('apostils__chunk')
            ch = Chunk.objects.filter(date__range=(start_date, stop_date), apostils__isnull=False).select_related('apostils')
            for c in ch:
                print(f"{c=}")
            print(f"{ch.values('date', 'time', 'apostils__fio', 'apostils__count_docs')}")
            return redirect('report')
    else:
        form = GenerateChunkForm()

    return render(request, 'apostil/report_dev.html', {'form': form})

# def getpdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="file.pdf"'
#     p = canvas.Canvas(response)
#     p.setFont("Courier", 20)
#     p.drawString(100,700, "Hi, security. Привет!")
#     p.showPage()
#     p.save()
#     return response
#
# def get_xlsx(request):
#     response = HttpResponse(content_type='application/xlsx')
#     response['Content-Disposition'] = f'attachment; filename="today.xlsx"'
#     pass



class Stat(ListView):
    ''' Список всех записей. всех-всех.'''
    model = Chunk
    template_name = 'apostil/stat.html'
    context_object_name = 'all_apostil'

    def __init__(self):
        super(ListChunk2, self).__init__()
        self.today = datetime.today()
        self.pre_monday = self.today + relativedelta(weekday=MO(-2))
        self.pre_friday = self.today + relativedelta(weekday=FR(-1))

    def get_queryset(self):
        apostils = Chunk.objects.filter(date__range=(self.pre_monday, self.today)).aggregate(docs=Sum('apostils__count_docs'))
        return apostils

    def get_context_data(self, **kwargs):
        context = super(Stat, self).get_context_data(**kwargs)
        context['pre_week_count'] = Chunk.filter(date).sele

