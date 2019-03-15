#
# Tesseract 4 OCR Runtime Environment - Docker Container
#

# Basic Tesseract runtime setup
FROM ubuntu:18.04

RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository -y ppa:alex-p/tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr-eng
RUN apt-get install -y wget

# As an extra dependency we need the digits only 
RUN ["wget", "https://github.com/Shreeshrii/tessdata_shreetest/raw/master/digits_comma.traineddata", "-P","/usr/share/tesseract-ocr/4.00/tessdata"]
RUN ["ls","/usr/share/tesseract-ocr/4.00/tessdata"]
ENV TESSDATA_PREFIX /usr/share/tesseract-ocr/4.00/tessdata

# This could be anything, will need improvement
RUN mkdir /home/work
WORKDIR /home/work
COPY tests/xp_captured.png /home/work/xp_captured.png

# Let's run Tesseract, and just output the results onto the console first.
CMD ["tesseract", "/home/work/xp_captured.png", "stdout","-l", "digits_comma","--psm","8"]