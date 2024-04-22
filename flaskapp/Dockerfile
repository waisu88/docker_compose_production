FROM python:3.9

EXPOSE 80/tcp
EXPOSE 443/tcp

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && python -m pip install -r requirements.txt 
EXPOSE 5000

EXPOSE 8003/tcp

COPY . /app