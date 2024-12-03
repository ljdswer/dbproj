FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY src .

EXPOSE 5000

WORKDIR /usr/src
COPY config ./config
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "app:create_app()" ]
