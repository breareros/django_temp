from django.urls import path
from .views import index, AddApostil, EditApostil, AllApostil, ListChunk, AddApostiWithDate, gen_chunks, \
    ListAllChunk

urlpatterns = [
    path('edit_apostil/<int:pk>/', EditApostil.as_view(), name='edit_apostil'),

    path('apostil_list/', AllApostil.as_view(), name='apostil_list'),
    path('add_apostil/<int:id_chunk>/', AddApostiWithDate.as_view(), name='add_apostil'),

    # path('chunk_list/<str:date>/<str:time>/', ListChunk.as_view(), name='chunk_list'),
    path('chunk_list/', ListChunk.as_view(), name='chunk_list'),
    path('all_chunk_list/', ListAllChunk.as_view(), name='all_chunk_list'),
    path('chunk_generate/', gen_chunks, name='chunk_generate'),

    path('', ListChunk.as_view()),
]