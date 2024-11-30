FROM python:3.12.7-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["gunicorn", "-b", "0.0.0.0:5050", "run:app"]