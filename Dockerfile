FROM python:3.8

# mettre l'heure à Paris
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

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



