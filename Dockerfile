# set base image
FROM python:3

# ensures that the python output is sent straight to terminal
ENV PYTHONUNBUFFERED=1

# create and set the working directory in the container
RUN mkdir /code
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt /code/

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local app directory to the working directory
COPY . /code/