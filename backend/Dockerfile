FROM python:3.8

WORKDIR /backend

COPY django/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY django .

# CMD python manage.py makemigrations
# CMD python manage.py migrate
# CMD python manage.py runserver 0.0.0.0:28172

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/backend/entrypoint.sh", "localhost" ]

EXPOSE 8000
