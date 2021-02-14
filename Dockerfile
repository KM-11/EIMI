FROM debian:latest

WORKDIR /app
RUN apt-get update && apt-get -y install python3 python3-pip python3-libvirt libvirt-dev

COPY ./ .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
