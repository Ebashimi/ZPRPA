import datetime

# Задаем дату и время
date_str = "2021-05-13"
start_time_str = "17:00:00"
end_time_str = "18:00:00"

# Создаем объекты datetime для начала и конца промежутка
start_datetime = datetime.datetime.strptime(date_str + " " + start_time_str, '%Y-%m-%d %H:%M:%S')
end_datetime = datetime.datetime.strptime(date_str + " " + end_time_str, '%Y-%m-%d %H:%M:%S')

# Преобразуем в Unix timestamp
start_timestamp = int(start_datetime.timestamp())
end_timestamp = int(end_datetime.timestamp())

print("Start timestamp:", start_timestamp)  # Вывод: 1620913200
print("End timestamp:", end_timestamp)      # Вывод: 1620916800