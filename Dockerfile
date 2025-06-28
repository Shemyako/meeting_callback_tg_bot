# Используем официальный Python 3.12 slim образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .

RUN apt update && apt install -y git

RUN pip install --no-cache-dir -r requirements.txt

RUN apt purge -y git \
    && apt autoremove -y \
    && apt clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Копируем файлы проекта
COPY . /app

# Запуск бота (предполагаем, что входная точка main.py)
CMD ["python", "-m", "src.bot"]
