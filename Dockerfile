FROM ubuntu

RUN apt-get sudo
RUN sudo apt-get update
RUN sudo apt-get install python3-pip

COPY ./app /

EXPOSE 80

CMD ["python3", "application.py"]
