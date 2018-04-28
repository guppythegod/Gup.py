# The Gup.py URL Shortnening Service

This is my take on a url shortning service using python, flask, and sqlite.

If you would like to see how it works, there are two ways:

##### Method One: Docker

1. Pull the docker image

`docker pull guppythegod/gup.py:latest`

2. Run the image with port 80

'docker run -p 80:80 guppythegod/pu.py'

##### Method Two: From Source

You will need python 3 for this project

1. Clone the repository

`git clone http://github.com/guppythegod/gup.py.git`

2. Change directory to working directory

`cd Gup.py/app`

3. Install pip dependencies

`python3 -m pip install -r requirements.txt`

4. Clear existing database

`python3 clear_database.py`

5. Create a new table

`python3 create_url_data_table.py`

6. Run application on port 80

`python3 application.py`

Thats it, Enjoy!
