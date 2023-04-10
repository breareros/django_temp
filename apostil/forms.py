from datetime import datetime, timedelta

from django import forms
from django.db.models import Q

from . import base
from .models import ApostilList, Chunk


class AddApostilForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['chunk'].empty_label = "Дата не выбрана"

    class Meta:
        model = ApostilList
        fields = ['fio', 'phone', 'count_docs', 'comments', 'chunk', 'is_gone', 'is_done']
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'count_docs': forms.NumberInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
            'is_gone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'chunk': forms.Select(attrs={'class': 'form-select'}),
        }


class AddApostiWithDateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = ApostilList
        fields = ['fio', 'phone', 'count_docs', 'comments', 'is_gone', 'is_done']
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'count_docs': forms.NumberInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
            'is_gone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EditApostilForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        limit_days = base.limit_days
        super().__init__(*args, **kwargs)
        self.fields['chunk'] = forms.ModelChoiceField(
            queryset=Chunk.objects.filter(
                Q(pk=self.instance.chunk_id) |
                Q(date__range=(datetime.today(), datetime.today() + timedelta(days=limit_days))) &
                Q(apostils__isnull=True)
            ),
            label='Слот времени',
            empty_label='Дата не выбрана',
            widget=forms.Select(attrs={'class': 'form-select'}))
        self.fields['chunk'].empty_label = "Дата не выбрана"

    class Meta:
        model = ApostilList
        fields = '__all__'
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'count_docs': forms.NumberInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control'}),
            'is_gone': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_done': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'chunk': forms.Select(attrs={'class': 'form-select'}),
        }


class GenerateChunkForm(forms.Form):
    start = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Начало периода',
    )
    end = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Конец периода',
    )

    def clean(self):
        super().clean()
        if self.cleaned_data.get('end') < self.cleaned_data.get('start'):
            raise forms.ValidationError('Дата конца периода должна быть позже даты начала')

        # Да так то проверка не нужна, функция не создаст расписание на выходные
        for date in (self.cleaned_data.get('start'), self.cleaned_data.get('end')):
            print(f"{date} {date.isoweekday()}")
            if date.isoweekday() in (6, 7):
                # raise forms.ValidationError(f" {date} Выходной или праздничный день")
                msg = f" {date} Выходной или праздничный день"
                self.add_error('end', msg)

        return self.cleaned_data
