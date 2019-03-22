FROM ubuntu:18.10

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
RUN apt-get update && apt-get install -y python3-pip

# https://stackoverflow.com/questions/47113029/importerror-libsm-so-6-cannot-open-shared-object-file-no-such-file-or-directo
# E   ImportError: libSM.so.6: cannot open shared object file: No such file or directory
RUN apt-get install -y libsm6 libxext6

# Fiying issue: ImportError: libXrender.so.1: cannot open shared object file: No such file or directory
# https://www.cyberciti.biz/faq/debian-ubuntu-linux-wkhtmltopdf-error-while-loading-shared-libraries-libxrender-so-1/
RUN apt-get install libfontconfig1 libxrender1

RUN pip3 install -r requirements/testing_linux_compatible.txt

# LETS GO MARIO
CMD pytest --junitxml=/home/work/junit/test-results.xml