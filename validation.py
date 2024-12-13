from fastapi import FastAPI
from fastapi import Path
from typing import Annotated

srv = FastAPI()  # создание объекта/приложения


@srv.get('/')  # хэндлер обработки обращения к главной странице
async def main_answer() -> str:
    return 'Главная страница'


@srv.get('/user/admin')  # хэндлер обработки обращения к странице администратора
async def admin_answer() -> str:
    return 'Вы вошли как администратор'


@srv.get('/user/{user_id}')  # хэндлер обработки обращения к странице пользователя
async def user_answer(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID')]) -> str:
    return f'Вы вошли как пользователь № {user_id}'


@srv.get('/user')  # хэндлер обработки запроса данных о пользователе
async def user_info(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter Username')],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter age')]) -> str:
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'
