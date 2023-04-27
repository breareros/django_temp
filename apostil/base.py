from datetime import date, datetime

white_ip_range = [f"10.24.12.{x}" for x in range(254)]

time_intervals = ['9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30']
limit_days = 14

executors = (
    (None, ''),
    ('r7200000-usr-eimorozova', 'Морозова Елена Ивановна'),
    ('r7200000-usr-evkozina', 'Козина Екатерина Витальевна'),
    ('r7200000-usr-oaplehanova', 'Плеханова Ольга Александровна'),
    # ('r7200000-usr-iiivanov', 'Иванов Иван Иванович'),
    # ('r7200000-usr-pppetrov', 'Петров Петр Петрович'),
    # ('r7200000-usr-sssidorov', 'Сидоров Сидор Сидорович'),
)


def holydays() -> dict[date]:
    holydays = [
    '2023-05-01',
    '2023-05-08',
    '2023-05-09',
    '2023-06-12',
    '2023-11-06'
]
    return [datetime.strptime(str(d), "%Y-%m-%d").date() for d in holydays]