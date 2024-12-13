from fastapi import FastAPI

srv = FastAPI()  # создание объекта/приложения


@srv.get('/')  # хэндлер обработки обращения к главной странице
async def main_answer() -> str:
    return 'Главная страница'


@srv.get('/user/admin')  # хэндлер обработки обращения к странице администратора
async def admin_answer() -> str:
    return 'Вы вошли как администратор'


@srv.get('/user/{user_id}')  # хэндлер обработки обращения к странице пользователя
async def user_answer(user_id: int) -> str:
    return f'Вы вошли как пользователь № {user_id}'


@srv.get('/user')  # хэндлер обработки запроса данных о пользователе
async def user_info(username: str, age: int) -> str:
    return f'Информация о пользователе. Имя: {username}, Возраст: {age}'
