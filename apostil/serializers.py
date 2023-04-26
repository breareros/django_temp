# from django.db.models import Count
# from rest_framework.serializers import ModelSerializer, SerializerMethodField
# from apostil.models import Chunk, ApostilList
#
# class ChunkSerializer(ModelSerializer):
#     class Meta:
#         model = Chunk
#         fields = '__all__'
#
# class ChunkApostilSerializer(ModelSerializer):
#     apostils = SerializerMethodField()
#     # days_count_doc = SerializerMethodField()
#     count = 0
#     rez = []
#     def get_apostils(self, instance):
#         print(f"{instance.pk} {instance.date} {instance.time} {self.count}")
#         self.rez = (ApostilList.objects.filter(chunk=instance.pk).annotate(total=Count('chunk__date', distinct=True)).values('chunk__time', 'fio', 'count_docs', 'phone', 'is_done'))
#         print(f"{instance.time} : {self.rez}\n")
#         self.count += 1
#         return self.rez
#
#     class Meta:
#         model = Chunk
#         fields = ['date', 'apostils']