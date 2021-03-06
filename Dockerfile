# GETS THE LATEST UBUNTU IMAGE
FROM ubuntu

# UPDATES
RUN apt-get update

# INSTALLS PYTHON
RUN apt-get install python3-pip

# COPIES APPLICATION FILES TO CONTAINER
COPY ./app /

# INSTALLS THE REQUIREMENTS FILE
RUN python3 -m pip install -r requirements.txt

# OPENS PORT 80 FOR INCOMING & OUTGOING
EXPOSE 80

# RUNS THE SERVER FILE
CMD ["python3", "application.py"]
