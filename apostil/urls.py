from django.urls import path
# from rest_framework.routers import SimpleRouter

from .views import AddApostil, EditApostil, AllApostil, ListChunk, AddApostilWithDate, gen_chunks, \
    ListAllChunk, report, ListChunk2, ListChunkOhrana

#    ChunkViewSet\
    #, ChunkAPIList

urlpatterns = [
    path('apostil_list/', AllApostil.as_view(), name='apostil_list'),
    path('add_apostil/<int:id_chunk>/', AddApostilWithDate.as_view(), name='apostil_add'),
    path('add_apostil/', AddApostil.as_view(), name='apostil_add_clean'),
    path('edit_apostil/<int:pk>/', EditApostil.as_view(), name='apostil_edit'),

    # path('chunk_list/<str:date>/<str:time>/', ListChunk.as_view(), name='chunk_list'),
    path('chunk_list/', ListChunk.as_view(), name='chunk_list_2'), # тут робить живой поиск т.к. одна таблица
    path('chunk_list_2/', ListChunk2.as_view(), name='chunk_list'),  # разбивка на таблицы с подсчетом документов на день, без поиска
    path('all_chunk_list/', ListAllChunk.as_view(), name='chunk_list_all'), # НЕДОДЕЛКА список всех сгененрированных чанков
    path('chunk_generate/', gen_chunks, name='chunk_generate'),

    path('report/', report, name='report'), #  TODO: реализовать отчеты
    # path('stat/', stat, name='stat'),
    path('ohrana/', ListChunkOhrana.as_view(), name='ohrana'),
    # path('pdf', getpdf, name='pdf'),

    path('', ListChunk2.as_view(), name='index'),

    # path('api/v1/cl/', ChunkAPIList.as_view()),
]

# router = SimpleRouter()
# router.register(r'api/chunk', ChunkViewSet, basename='chunk')
#
# urlpatterns += router.urls