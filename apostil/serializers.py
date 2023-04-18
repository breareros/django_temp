from django.db.models import Sum
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apostil.models import ApostilList, Chunk

class ApostilListSerializer(ModelSerializer):
    class Meta:
        model = ApostilList
        fields = '__all__'


class ChunkSerializer(ModelSerializer):
    class Meta:
        model = Chunk
        fields = '__all__'

class ChunkApostilSerializer(ModelSerializer):
    docDayCount = serializers.SerializerMethodField()
    apostils = serializers.SerializerMethodField()
    # phone = serializers.SerializerMethodField()

    class Meta:
        model = Chunk
        fields = ['id', 'date', 'docDayCount', 'apostils']

    def get_docDayCount(self, instance):
        # return Chunk.objects.filter().prefetch_related('apostils').select_related('apostils__chunk')
        return Chunk.objects.filter(date=instance.date).aggregate(docs=Sum('apostils__count_docs'))

    def get_apostils(self, instance):
        # return Chunk.objects.filter(date=instance.date).prefetch_related('apostils').select_related('apostils__fio').values_list()
        # return Chunk.objects.filter(date=instance.date).prefetch_related('apostils').values_list(
        return Chunk.objects.filter(date=instance.date).prefetch_related('apostils').values_list(
            # 'date',
            'time',
            'apostils__fio',
            'apostils__count_docs',
            'apostils__phone',
            'apostils__is_done',
        )