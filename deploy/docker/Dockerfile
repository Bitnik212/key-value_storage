FROM python:3.10
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app
RUN ssh-keygen -m PKCS8 -f publickey.pem -i > publickey.pub
CMD ["gunicorn", "main:app", "-c", "gunicorn_conf.py"]
