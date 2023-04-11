from datetime import date, datetime, timedelta

from apostil import base
from apostil.models import Chunk


def generate_chunks(start_date: date, end_date: date,
                    time_intervals: list = base.time_intervals) -> None:
    delta = end_date - start_date
    print(f"{delta}, {type(delta)}: {type(start_date)} {type(end_date)}")
    chunks_to_create = []
    for i in range((end_date - start_date).days + 1):
        current_date = start_date + timedelta(days=i)
        if current_date.isoweekday() not in (6, 7):  # 6 - суббота, 7 - воскресение
            chunks_to_create += [Chunk(date=current_date, time=datetime.strptime(t, '%H:%M').time()) for t in
                                 time_intervals]

    # Получаем список уже существующих чанков в периоде start_date - end_date
    existing_chunks = Chunk.objects.filter(date__range=(start_date, end_date))

    # Отфильтровываем из списка чанков те, которые уже были созданы ранее
    chunks_to_create = [chunk for chunk in chunks_to_create if
                        not existing_chunks.filter(date=chunk.date, time=chunk.time).exists()]

    # Создаем новые чанки в базе данных
    if chunks_to_create:
        print(chunks_to_create)
        Chunk.objects.bulk_create(chunks_to_create)