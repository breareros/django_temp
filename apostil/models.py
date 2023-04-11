from datetime import datetime

from django.db import models
from django.urls import reverse

from apostil import base


# Create your models here.
class ApostilList(models.Model):
    fio = models.CharField(max_length=300, null=False, verbose_name='ФИО заявителя')
    count_docs = models.PositiveIntegerField(default=1, verbose_name='Количество документов')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания записи')
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name='Телефон')
    comments = models.TextField(null=True, blank=True, verbose_name='Примечания')
    is_done = models.BooleanField(default=False, verbose_name="Документы предоставлены")
    is_gone = models.BooleanField(default=False, verbose_name="Не явились")
    executor_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Исполнитель') # , choices=base.executors)
    chunk = models.OneToOneField('Chunk', on_delete=models.CASCADE, related_name='apostils', blank=True, null=True,
                                 verbose_name='Слот времени')

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse(None, kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'
        ordering = ['-chunk']


class Chunk(models.Model):
    time_intervals = [(datetime.strptime(time, '%H:%M').time(), time) for time in base.time_intervals]
                      # ['9:00', '9:15', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30']]

    date = models.DateField(auto_created=False, null=False,
                            verbose_name='Дата приема')
    time = models.TimeField(verbose_name="Время приема", null=True, choices=time_intervals)

    def __str__(self):
        return f"{self.date} {self.time}"

    class Meta:
        verbose_name = 'Дата время приема'
        verbose_name_plural = 'Даты время приема'
        ordering = ['date', 'time']
        unique_together = ['date', 'time']
