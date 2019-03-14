# Automate Diablo 1 with Python + OpenCV

[![Build Status](https://dev.azure.com/hosszub/evil_snek/_apis/build/status/hosszubalazs.evil_snek?branchName=master)](https://dev.azure.com/hosszub/evil_snek/_build/latest?definitionId=1&branchName=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=hosszubalazs_evil_snek&metric=alert_status)](https://sonarcloud.io/dashboard?id=hosszubalazs_evil_snek)

This repository is an attempt at creating a bot that plays Diablo 1. The game is only analysed from it's UI, not by direct memory access. The repository is in a super-early stage, with nothing useful in it for the moment.

This idea is heavily based on : [Python plays Grand Theft Auto V](https://www.youtube.com/watch?v=ks4MPfMq8aQ)

## User Guide

The project only works on Microsoft Windows operating system. As Diablo is only released for Windows, this should not be an issue.

1. Obtain [Diablo](https://www.gog.com/game/diablo) from GoG
1.1 Use a 32 bit Python 3.x
2. Checkout the repository, activate the virtual environment, install dependencies
3. Install Tesseract 4.0 64 bit binary from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki). Add `tesseract.exe` to your path. You can also check the [PyTesseract](https://pypi.org/project/pytesseract/) installation guide.
4. Start Diablo in windowed mode in 640x480. Diablo should appear in the center of the screen.
5. Start the app: `python app.py`
6. Marvel in the beauty and uselessness of the currently available OpenCV filters

## Current state

A proof-of-concept feedback loop is in place. User interactions (mouse clicks and keyboard presses) can be sent to the game. using this technique the character tabs is opened and screenshotted. After cropping for the intersting part of the image, the number of current experience is determined by OCR. This number is logged into a temporary CSV file. The character is not controlled in any way yet, using clicks that should be possible.
The plan is to focus on a minimum viable solution for a warrior character. (probably following a very simple 1h weapon+shield strategy). As the solution matures it might be possible:

- for a single character to be dynmically ready for multiple strategies
- to make the framework moddable, making it easy to develop AI for separate classes and strategies

## Tooling

- [MSS](https://pypi.org/project/mss/) -> Grab the screenshot of the game, [docs here help a lot](https://python-mss.readthedocs.io/examples.html#opencv-numpy)
- [OpenCV 4.0](https://pypi.org/project/opencv-python/) -> Process the image stream
- [Python ctypes](https://www.google.com/search?client=firefox-b-d&q=pzthon+ctzpes), WIN32 API PostMessage --> Send keyboard and mouse events to the window, simulating user input
- [Tesseract](https://github.com/tesseract-ocr/tesseract), through [pytesseract](https://pypi.org/project/pytesseract/) --> Optical Character recognition (OCR).
  
## Automating keyboard and mouse messages

Automating the UI events to Diablo, a DirectX game, was challenging, altough looking back it is pretty simple. Instead of spending hours googling for partially working solutions I suggest the analytical approach. There is a neat tool called Spy++, distributed as a tool of Visual Studio, to watch the window of Diablo and log the messages that it receives. The proper events, both for keyboard and mouse actions, will be nicely logged. MSDN documentation will help to understand what are all those parameters for the messages. The resulting code might not be super nice, but it will work.

## Grand plan

The solution is based on divide and conquer. The solution will rotate across the module. Each module is a flow / iteration of measure, plan, act. We need to solve the following modules:

### Inventory management

Based on the current contents of the inventory, equip the best gear. "Best" depends heavily on the class, and a specific strategy within the class, for example a warrior with one handed weapons.

### Fighting

Identify enemies. Kill enemies. Collect the loot and gold. Understand if inventory is full. Most importantly: don't die.
As an advanced feature: understand enemy resistances. Later on in the game certain enemies can only be killed with certain damage types. This might require advanced inventory management, keeping in stock multiple weapons.

### Shopping

Return to town. Recover health. Sell extra items. Repair items. Spend money, buy additional items.

### Leveling up

Managing the character, allocating character points. The ideal distribution is heavily dependent on the exact strategy of the character. Needs to work well together with inventory management, as items have certain requirements.

## Tesseract notes

1. Diablo is using the [Exocet](https://fonts.adobe.com/fonts/exocet) font. The basic dictionary [was not trained](https://github.com/tesseract-ocr/tesseract/blob/master/src/training/language-specific.sh) with this font, but nevertheless Tesseract seems to function good enough for recognising the number
2. Cut tight! A good cut is worth more then filtering.
3. Use the correct PSM mode, ideally PSM 8 for single word (even for numbers)
4. If you are expecting only digits, download and use the [user-made digits-only dictionary](https://github.com/Shreeshrii/tessdata_shreetest). Tesseract 4 [does not support](https://github.com/tesseract-ocr/tesseract/issues/751) whitelist/blacklist.
5. Low resolution (running in 640#480 window) does not seem to be an issue. So far when manually cut, numbers were correctly analysed even without any picture processing!

Further resource : [An Overview of the Tesseract OCR Engine](http://static.googleusercontent.com/media/research.google.com/en//pubs/archive/33418.pdf)
