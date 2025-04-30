# syntax=docker/dockerfile:1
FROM ubuntu:22.04

COPY . /project_files
WORKDIR /project_files

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]