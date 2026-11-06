import requests

url = "http://127.0.0.1:5000"


# GET /
r = requests.get(f"{url}/")
print(r.status_code, r.text[:40])          # 200 <h1>Гостевая книга</h1>


# POST /notes — создание и валидация
r = requests.post(f"{url}/notes", json={"author": "Иван", "text": "Привет"})
print(r.status_code, r.json())             # 201 {'id': 1, 'author': 'Иван', 'text': 'Привет', 'likes': 0}
note1 = r.json()["id"]

r = requests.post(f"{url}/notes", json={"author": "Иван", "text": "Вторая"})
print(r.status_code, r.json())             # 201
note2 = r.json()["id"]

r = requests.post(f"{url}/notes", json={"author": "Пётр", "text": "От другого"})
print(r.status_code, r.json())             # 201
note3 = r.json()["id"]

r = requests.post(f"{url}/notes", json={"author": "Иван", "text": "Пойдёт под DELETE по id"})
print(r.status_code, r.json())             # 201
note4 = r.json()["id"]

r = requests.post(f"{url}/notes", json={"author": "Иван"})              # нет text
print(r.status_code, r.json())             # 400 {'error': "field 'text' ..."}

r = requests.post(f"{url}/notes", json={"text": "без автора"})          # нет author
print(r.status_code, r.json())             # 400 {'error': "field 'author' ..."}

r = requests.post(f"{url}/notes", json={"author": "Иван", "text": ""})  # пустой text
print(r.status_code, r.json())             # 400

r = requests.post(f"{url}/notes", json={"author": "", "text": "x"})      # пустой author
print(r.status_code, r.json())             # 400

r = requests.post(f"{url}/notes", json={"author": "Иван", "text": "   "})  # только пробелы
print(r.status_code, r.json())             # 400

r = requests.post(f"{url}/notes", data={"text": "x"})                   # form-data, не JSON
print(r.status_code, r.json())             # 400


# GET /notes и GET /notes/<id>
r = requests.get(f"{url}/notes/{note1}")
print(r.status_code, r.json())             # 200

r = requests.get(f"{url}/notes/999999")
print(r.status_code, r.json())             # 404 {'error': 'not found'}

r = requests.get(f"{url}/notes/abc")
print(r.status_code, r.json())             # 404 (не <int:>)

r = requests.get(f"{url}/notes?author=Иван")
print(r.status_code, r.json())             # 200 — только заметки Ивана

r = requests.get(f"{url}/notes?author=Никто")
print(r.status_code, r.json())             # 200 []

r = requests.get(f"{url}/notes?sort=likes&order=desc")
print(r.status_code, r.json())             # 200 — по лайкам убывание

r = requests.get(f"{url}/notes?sort=id&order=desc")
print(r.status_code, r.json())             # 200 — свежие сверху

r = requests.get(f"{url}/notes?limit=2&offset=1")
print(r.status_code, r.json())             # 200 — 2 штуки, пропустив 1

r = requests.get(f"{url}/notes?sort=text")
print(r.status_code, r.json())             # 400 {'error': "sort must be 'id' or 'likes'"}

r = requests.get(f"{url}/notes?order=up")
print(r.status_code, r.json())             # 400

r = requests.get(f"{url}/notes?limit=0")
print(r.status_code, r.json())             # 400

r = requests.get(f"{url}/notes?limit=101")
print(r.status_code, r.json())             # 400

r = requests.get(f"{url}/notes?limit=abc")
print(r.status_code, r.json())             # 400

r = requests.get(f"{url}/notes?offset=-1")
print(r.status_code, r.json())             # 400

r = requests.get(f"{url}/notes?offset=xyz")
print(r.status_code, r.json())             # 400


# PUT /notes/<id> — полная замена (author + text)
r = requests.put(f"{url}/notes/{note1}",
                 json={"author": "Иван", "text": "Обновлено через PUT"})
print(r.status_code, r.json())             # 200

r = requests.put(f"{url}/notes/{note1}", json={"text": "без автора"})
print(r.status_code, r.json())             # 400

r = requests.put(f"{url}/notes/{note1}", json={"author": "Иван"})
print(r.status_code, r.json())             # 400

r = requests.put(f"{url}/notes/999999",
                 json={"author": "Иван", "text": "x"})
print(r.status_code, r.json())             # 404


# PATCH /notes/<id> — только text
r = requests.patch(f"{url}/notes/{note2}", json={"text": "Правка через PATCH"})
print(r.status_code, r.json())             # 200

r = requests.patch(f"{url}/notes/{note2}", json={"author": "Пётр"})
print(r.status_code, r.json())             # 400 — нет text

r = requests.patch(f"{url}/notes/{note2}", json={"text": ""})
print(r.status_code, r.json())             # 400

r = requests.patch(f"{url}/notes/999999", json={"text": "x"})
print(r.status_code, r.json())             # 404


# POST /notes/<id>/like
r = requests.post(f"{url}/notes/{note1}/like")
print(r.status_code, r.json())             # 200 likes=1

r = requests.post(f"{url}/notes/{note1}/like")
print(r.status_code, r.json())             # 200 likes=2

r = requests.post(f"{url}/notes/{note1}/like")
print(r.status_code, r.json())             # 200 likes=3

r = requests.post(f"{url}/notes/{note3}/like")
print(r.status_code, r.json())             # 200 likes=1

r = requests.post(f"{url}/notes/999999/like")
print(r.status_code, r.json())             # 404


# GET /authors — статистика
r = requests.get(f"{url}/authors")
print(r.status_code, r.json())             # 200 [{'author': 'Иван', 'notes': 3, 'likes': 3},
                                           #      {'author': 'Пётр', 'notes': 1, 'likes': 1}]


# DELETE /notes/<id>
r = requests.delete(f"{url}/notes/{note4}")
print(r.status_code, r.text)               # 204 (тело пустое)

r = requests.delete(f"{url}/notes/{note4}")
print(r.status_code, r.json())             # 404 — уже удалено

r = requests.delete(f"{url}/notes/999999")
print(r.status_code, r.json())             # 404


# DELETE /notes?author=<имя> — массовое удаление
r = requests.delete(f"{url}/notes")
print(r.status_code, r.json())             # 400 — нет author

r = requests.delete(f"{url}/notes?author=")
print(r.status_code, r.json())             # 400 — пустой

r = requests.delete(f"{url}/notes?author=%20%20")
print(r.status_code, r.json())             # 400 — только пробелы

r = requests.delete(f"{url}/notes?author=Иван")
print(r.status_code, r.json())             # 200 {'deleted': 2} (note1, note2)

r = requests.delete(f"{url}/notes?author=Иван")
print(r.status_code, r.json())             # 200 {'deleted': 0}


# 405 Method Not Allowed
r = requests.post(f"{url}/notes/{note3}")        # у /notes/<id> нет POST
print(r.status_code, r.json())             # 405 {'error': 'method not allowed'}

r = requests.get(f"{url}/notes/{note3}/like")    # у like нет GET
print(r.status_code, r.json())             # 405

r = requests.put(f"{url}/notes")                 # у /notes нет PUT
print(r.status_code, r.json())             # 405

r = requests.delete(f"{url}/")                   # у / только GET
print(r.status_code, r.json())             # 405


# Финальное состояние
r = requests.get(f"{url}/notes?limit=100")
print(r.status_code, r.json())             # 200 — остался только Пётр

r = requests.get(f"{url}/authors")
print(r.status_code, r.json())             # 200 [{'author': 'Пётр', 'notes': 1, 'likes': 1}]