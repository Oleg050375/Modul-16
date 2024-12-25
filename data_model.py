from fastapi import FastAPI
from fastapi import Path
from fastapi import HTTPException
from typing import Annotated
from pydantic import BaseModel

srv = FastAPI()  # создание объекта/приложения

users = []  # список пользователей


class User(BaseModel):  # класс данных пользователя
    id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]
    username: Annotated[str, Path(min_length=5, max_length=20, description='Enter Username')]
    age: Annotated[int, Path(ge=18, le=120, description='Enter age')]


@srv.get('/users')  # хэндлер обработки запроса списка пользователей
async def list_answer() -> list:
    return users


@srv.post('/user/{username}/{age}')  # хаэндлер обработки запроса на создание нового пользователя
async def add_user(username: str, age: int) -> User:
    id_list = []  # список всех id
    for i in users:  # цикл наполнения списка всех id
        id_list.append(i.id)
    if len(id_list) == 0:  # проверка на пустой список всех id
        new_id = 1
    else:
        new_id = max(id_list) + 1  # определение id следующего пользователя
    try:
        a = User(id=new_id, username=username, age=age)  # формирование объекта новой записи
        users.append(a)  # добавление записи в список пользователей
        return a  # возврат объекта новой записи
    except IndexError:
        raise HTTPException(status_code=404, detail='Ошибка формата данных')


@srv.put('/user/{user_id}/{username}/{age}')  # хаэндлер обработки запроса на изменение записи
async def ex_user(user_id: int, username: str, age: int) -> User:
    try:
        flag = 0
        a = None
        for i in users:  # цикл перебора записей
            if i.id == user_id:  # сравнение/поиск id
                i.username = username  # изменение имени пользователя
                i.age = age  # изменение возраста пользователя
                flag = 1
                a = i
                break  # выход из цикла
            else:
                continue
        if flag == 1:
            return a  # возврат объекта изменённой записи
        else:
            return f'The user {user_id} not found.'
    except IndexError:
        raise HTTPException(status_code=404, detail='Пользователь не найден')


@srv.delete('/user/{user_id}')  # хаэндлер обработки запроса на удаление записи
async def del_user(user_id: int) -> User:
    try:
        flag = 0
        cnt = 0  # счётчик
        a = None
        for i in users:  # цикл перебора записей
            if i.id == user_id:  # сравнение/поиск id
                a = users.pop(cnt)  # удаление записи
                flag = 1
                break  # выход из цикла
            else:
                cnt = cnt + 1  # инкремент счётчика
        if flag == 1:
            return a  # возврат объекта удалённой записи
        else:
            return f'The user {user_id} not found.'
    except IndexError:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
