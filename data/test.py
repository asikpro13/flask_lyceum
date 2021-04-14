from requests import get, post

print(get('http://127.0.0.1:8080/api/jobs').json())  # Получение всех работ
print(get('http://127.0.0.1:8080/api/jobs/3').json())  # Получение одной работы
print(get('http://127.0.0.1:8080/api/jobs/21д').json())  # Неверный id
print(get('http://127.0.0.1:8080/api/jobs/sad').json())  # Строка
print(post('http://127.0.0.1:8080/api/jobs/', json={
    'team_leader': '3',
    'job': 'ewd',
    'work_size': '1',
    'collaborators': '1, 2, 3',
    'is_finished': True,
    'id_creator': 3}
           ))