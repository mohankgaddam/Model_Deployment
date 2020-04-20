#Use python base image
FROM python:3.7-slim

#Set working directory
WORKDIR /app

#Copy current directory to working directory
ADD . /app

#Install required packages present in requirements.txt
RUN pip install -r requirements.txt

#open port for communication 
EXPOSE 5003

#Set Enviornment variable
ENV NAME FlaskApp

#Run the Application
CMD ["python", "app.py"]
