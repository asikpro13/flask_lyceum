from requests import get

print(get('http://127.0.0.1:8080/api/jobs').json())  # Получение всех работ
print(get('http://127.0.0.1:8080/api/jobs/3').json())  # Получение одной работы
print(get('http://127.0.0.1:8080/api/jobs/21д').json())  # Неверный id
print(get('http://127.0.0.1:8080/api/jobs/sad').json())  # Строка
