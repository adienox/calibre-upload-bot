FROM python:slim

WORKDIR /app
COPY requirements.txt requirements.txt

# install packages
RUN apt-get update && \
	pip3 install -r requirements.txt  && \
	apt-get remove --purge -y build-essential && \
	apt-get autoclean -y && apt-get autoremove -y && \
	rm -rf \
	/default/ \
	/etc/default/ \
	/tmp/* \
	/etc/cont-init.d/* \
	/var/lib/apt/lists/* \
	/var/tmp/* 

COPY main.py /app/main.py
COPY root/ /

RUN chmod 777 /app/main.py 
RUN chmod 777 -R /etc/services.d/

VOLUME /books /output /binaries
