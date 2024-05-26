from app import app, db
from app.models import User

# Включаем контекст приложения для работы с базой данных
app.app_context().push()

# Запрашиваем у пользователя логин и пароль
username: str = input("Введите логин пользователя: ")
password: str = input("Введите пароль пользователя: ")

# Создаем нового пользователя
u = User(username=username)  # Создаем класс из модели
u.set_password(password)  # Устанавливаем пароль пользователя с помощью метода модели

# Добавляем нового пользователя в сессию базы данных
db.session.add(u)

# Сохраняем изменения в базе данных
db.session.commit()

# Выводим сообщение о добавленном пользователе
print(f"Пользователь был добавлен: \nЛогин: {username}\nПароль: {password}")
