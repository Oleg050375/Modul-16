from fastapi import FastAPI, status, Body, Request, Form, Path, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from pydantic import BaseModel

srv = FastAPI()  # создание объекта/приложения

tmp = Jinja2Templates(directory='templates')  # создание объекта шаблонизатора

users = []  # список пользователей


class User(BaseModel):  # класс данных пользователя
    id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]
    username: Annotated[str, Path(min_length=5, max_length=20, description='Enter Username')]
    age: Annotated[int, Path(ge=18, le=120, description='Enter age')]


@srv.get('/')  # хэндлер обработки запроса списка пользователей
async def answer_list(request: Request) -> HTMLResponse:
    return tmp.TemplateResponse('users.html', {'request':request, 'users':users})


@srv.get('/user/{id}')  # хэндлер обработки запроса пользователя по id
async def answer_user(request:Request, user_id:int) -> HTMLResponse:
    try:
        flag = 0
        user = None
        for i in users:  # цикл перебора записей
            if i.id == user_id:  # сравнение/поиск id
                user = i
                flag = 1
                break  # выход из цикла
            else:
                continue
        if flag == 1:
            return tmp.TemplateResponse('users.html', {'request':request, 'user':user})
        else:
            return tmp.TemplateResponse('users.html', {'request': request, 'user': f'The user {user_id} not found.'})
    except IndexError:
        raise HTTPException(status_code=404, detail='Пользователь не найден')


@srv.post('/user/{username}/{age}')  # хаэндлер обработки запроса на создание нового пользователя
async def add_user(username: str, age: int) -> str:
    id_list = []  # список всех id
    for i in users:  # цикл наполнения списка всех id
        id_list.append(i.id)
    if len(id_list) == 0:  # проверка на пустой список всех id
        new_id = 1
    else:
        new_id = max(id_list) + 1  # определение id следующего пользователя
    try:
        users.append(User(id=new_id, username=username, age=age))  # добавление записи в список пользователей
        return f'User {new_id} is registered.'
    except IndexError:
        raise HTTPException(status_code=404, detail='Ошибка формата данных')


@srv.put('/user/{user_id}/{username}/{age}')  # хаэндлер обработки запроса на изменение записи
async def ex_user(user_id: int, username: str, age: int) -> str:
    try:
        flag = 0
        for i in users:  # цикл перебора записей
            if i.id == user_id:  # сравнение/поиск id
                i.username = username  # изменение имени пользователя
                i.age = age  # изменение возраста пользователя
                flag = 1
                break  # выход из цикла
            else:
                continue
        if flag == 1:
            return f'The user {user_id} is updated.'
        else:
            return f'The user {user_id} not found.'
    except IndexError:
        raise HTTPException(status_code=404, detail='Пользователь не найден')


@srv.delete('/user/{user_id}')  # хаэндлер обработки запроса на удаление записи
async def del_user(user_id: int) -> str:
    try:
        flag = 0
        cnt = 0  # счётчик
        for i in users:  # цикл перебора записей
            if i.id == user_id:  # сравнение/поиск id
                users.pop(cnt)  # удаление записи
                flag = 1
                break  # выход из цикла
            else:
                cnt = cnt + 1  # инкремент счётчика
        if flag == 1:
            return f'The user {user_id} is deleted.'
        else:
            return f'The user {user_id} not found.'
    except IndexError:
        raise HTTPException(status_code=404, detail='Пользователь не найден')