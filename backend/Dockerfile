FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN  pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host", "0.0.0.0"]