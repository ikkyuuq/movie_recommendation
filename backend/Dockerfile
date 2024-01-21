FROM python:3

WORKDIR /app

COPY app.py ./backend
COPY db.py ./backend
COPY models.py ./backend

COPY requirements.txt ./backend
RUN pip install --no-cache-dir -r ./backend/requirements.txt

EXPOSE 8000

CMD [ "python", "app.py" ]


