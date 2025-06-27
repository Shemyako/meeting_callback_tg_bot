# Используем официальный Python 3.12 slim образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . /app

# Запуск бота (предполагаем, что входная точка main.py)
CMD ["python", "-m", "src.bot"]
