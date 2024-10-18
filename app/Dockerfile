FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY config.toml .
COPY src .

EXPOSE 5000
CMD [ "gunicorn", "-b", "0.0.0.0:5000", "app:create_app()" ]
