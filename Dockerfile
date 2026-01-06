FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Dummy web server (Render ko port mil jaaye)
EXPOSE 8080

CMD python bot.py & python -m http.server 8080