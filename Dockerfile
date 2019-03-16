FROM ubuntu:18.10

# Install Tesseract
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:alex-p/tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr-eng
RUN apt-get install -y wget
# As an extra dependency we need the digits only 
RUN wget https://github.com/Shreeshrii/tessdata_shreetest/raw/master/digits_comma.traineddata -P /usr/share/tesseract-ocr/4.00/tessdata 
ENV TESSDATA_PREFIX /usr/share/tesseract-ocr/4.00/tessdata

# This could be anything, will need improvement
RUN mkdir /home/work
WORKDIR /home/work

# Checkout the project into the container
COPY evil_snek evil_snek
COPY requirements requirements
COPY tests tests
RUN mkdir junit

# Default Python 3.6 is good enough. Pip is needed still.
# no ned for venv, Docker is already a virtual environment
RUN apt-get install -y python3-pip

# https://stackoverflow.com/questions/47113029/importerror-libsm-so-6-cannot-open-shared-object-file-no-such-file-or-directo
# E   ImportError: libSM.so.6: cannot open shared object file: No such file or directory
RUN apt-get install -y libsm6 libxext6

RUN pip3 install -r requirements/testing_linux_compatible.txt

# LETS GO MARIO
CMD pytest --junitxml=/home/work/junit/test-results.xml