from fastapi import FastAPI
from fastapi import Path
from typing import Annotated

srv = FastAPI()  # создание объекта/приложения

users = {'1': 'Имя: Example, возраст: 18'}


@srv.get('/users')  # хэндлер обработки запроса списка пользователей
async def list_answer() -> dict:
    return users


@srv.post('/user/{username}/{age}')  # хаэндлер обработки запроса на создание нового пользователя
async def add_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter Username')],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> str:
    k = str(int(max(list(users.keys()))) + 1)  # определение ключа следующей записи
    users[k] = f'Имя: {username}, возраст: {age}'  # добавление новой записи
    return f'User {k} is registered.'


@srv.put('/user/{user_id}/{username}/{age}')  # хаэндлер обработки запроса на изменение записи
async def ex_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')],
                  username: Annotated[str, Path(min_length=5, max_length=20, description='Enter Username')],
                  age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> str:
    k = str(user_id)  # формирование ключа изменяемой записи
    users[k] = f'Имя: {username}, возраст: {age}'  # изменение записи
    return f'The user {k} is updated.'


@srv.delete('/user/{user_id}')  # хаэндлер обработки запроса на удаление записи
async def del_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]) -> str:
    k = str(user_id)  # формирование ключа удаляемой записи
    users.pop(k)  # удаление записи
    return f'The user {k} is deleted.'
