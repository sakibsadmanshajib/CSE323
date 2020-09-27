FROM python:3.8

COPY CSE323/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . code
WORKDIR /code

EXPOSE 8000

ENTRYPOINT [ "python", "CSE323/manage.py" ]
CMD [ "runserver", "0.0.0.0:8000" ]

