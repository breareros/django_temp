from django.urls import path
from .views import index, AddApostil, EditApostil, AllApostil, ListChunk, AddApostilWithDate, gen_chunks, \
    ListAllChunk, report, ListChunk2

urlpatterns = [
    path('apostil_list/', AllApostil.as_view(), name='apostil_list'),
    path('add_apostil/<int:id_chunk>/', AddApostilWithDate.as_view(), name='apostil_add'),
    path('add_apostil/', AddApostil.as_view(), name='apostil_add_clean'),
    path('edit_apostil/<int:pk>/', EditApostil.as_view(), name='apostil_edit'),

    # path('chunk_list/<str:date>/<str:time>/', ListChunk.as_view(), name='chunk_list'),
    path('chunk_list/', ListChunk.as_view(), name='chunk_list_2'),
    path('cl2/', ListChunk2.as_view(), name='chunk_list'),
    path('all_chunk_list/', ListAllChunk.as_view(), name='chunk_list_all'), # НЕДОДЕЛКА
    path('chunk_generate/', gen_chunks, name='chunk_generate'),

    path('report/', report, name='report'),

    path('', ListChunk2.as_view(), name='index'),
]