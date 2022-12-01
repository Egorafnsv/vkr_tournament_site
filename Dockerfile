FROM python

WORKDIR /app

COPY . .

EXPOSE 8000

RUN pip install Django
RUN pip install django-crispy-forms

VOLUME ["/app"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]