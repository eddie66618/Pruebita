FROM osgeo/gdal:ubuntu-full-3.6.3

ENV PYTHONUNBUFFERED=1

ENV TZ=America/Lima \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update 
RUN apt-get install tzdata

RUN echo "America/Lima" > etc/timezone
RUN ln -fs /usr/share/zoneinfo/America/Lima /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata 

WORKDIR /app

RUN apt-get update && apt-get -y install python3-pip --fix-missing

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

RUN pip install djangorestframework

RUN pip install djangorestframework-simplejwt

RUN pip install drf-yasg

RUN apt-get install python3-psycopg2

RUN pip install python-dateutil

RUN pip install django-cors

RUN pip install django-cors-headers 

RUN pip install pytz

RUN pip install tzdata

RUN pip install python-decouple

RUN pip install requests

RUN python -m pip install Pillow

RUN pip install django-cleanup

COPY ./ ./

CMD ["python", "manage.py", "runserver","0.0.0.0:8050"]


