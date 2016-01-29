FROM python:3.4.4-wheezy

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 5000

CMD ["python", "./manage.py", "runserver", "--host", "0.0.0.0"]
