FROM python:3.10.7-alpine3.16

# create and set working directory
WORKDIR /app

# copy files to working directory
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# si /app/data not exit create it
RUN if [ ! -d "/app/data" ]; then mkdir /app/data; fi

# enregistrer un volume pour le dossier /app/data
VOLUME /app/data

# run the command to start app
CMD ["python", "setup.py"]



