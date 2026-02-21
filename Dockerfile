FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir python-telegram-bot --upgrade

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]