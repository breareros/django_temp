from django.contrib import admin
from .models import ApostilList, Chunk

# Register your models here.
class ApostilListAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'count_docs', 'phone', 'comments', 'is_done', 'chunk', 'executor_name')
    list_display_links = ('fio', 'phone', 'is_done', 'executor_name' )
    search_fields = ('fio', 'phone', 'comments')

class ChunkAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time' )
    list_display_links = ('id', 'date', 'time')
    search_fields = ('id', 'date', 'time')

admin.site.register(ApostilList, ApostilListAdmin)
admin.site.register(Chunk, ChunkAdmin)
