# clone the repo
git clone https://github.com/asherif123/backend-task-rate-api.git

# create your virtual environment
python3 -m venv venv

# to activate the virtual env
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# run the tests
python manage.py test

# run the project
python manage.py runserver

##### DOCKER #####

# you can download my image and run it directly
https://drive.google.com/drive/folders/1oqy789BpoPxipXCgQgYlHKURBRBgHwgP?usp=sharing

# OR build the image
sudo docker-compose build

# run the image
sudo docker-compose up
