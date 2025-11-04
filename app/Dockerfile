FROM python:alpine

RUN mkdir /app
ADD ./app.py /app

WORKDIR /app


RUN apk update
RUN apk add --no-cache gcc musl-dev libffi-dev mariadb-dev

RUN pip install --upgrade pip
RUN pip install flask gunicorn mysqlclient


# CMD [ "gunicorn" ,"-b" , "0.0.0.0:5000","app:app"]
CMD gunicorn -b 0.0.0.0:5000 app:app