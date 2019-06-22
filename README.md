# Automate Diablo 1 with Python + OpenCV

[![Build Status](https://dev.azure.com/hosszub/evil_snek/_apis/build/status/hosszubalazs.evil_snek?branchName=master)](https://dev.azure.com/hosszub/evil_snek/_build/latest?definitionId=1&branchName=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=hosszubalazs_evil_snek&metric=alert_status)](https://sonarcloud.io/dashboard?id=hosszubalazs_evil_snek)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/hosszubalazs/evil_snek/master)

This repository is an attempt at creating a bot that plays Diablo 1. The game is only analysed from it's UI, not by direct memory access. The repository is in a super-early stage, with nothing useful in it for the moment.

This solution is heavily inspired by :

- [Python plays Grand Theft Auto V](https://www.youtube.com/watch?v=ks4MPfMq8aQ)
- [Credit card OCR with OpenCV and Python](https://www.pyimagesearch.com/2017/07/17/credit-card-ocr-with-opencv-and-python/)

Extra resource to check:
- [The Brood War API](https://bwapi.github.io/)

## Current state

### Understanding the game state

Character recognition is solved for numbers, please check the `docs` folder for Jupyter Notebooks for examples.
As a primer on computer vision I found the following page helpful: [Image Processing 101](https://codewords.recurse.com/issues/six/image-processing-101)

Convoltions, kernel size, blurring: https://www.youtube.com/watch?v=C_zFhWdM4ic

#### Character screen

[ocr_by_template_matching.ipynb](docs/ocr_by_template_matching.ipynb)

Running the application will analyse the character tab. It will automatically be opened, taken a screenshot of, and closed, every 3 seconds.
The screenshot is used for further analysis. Several properties are analysed, like experience and health. Please check the tests for up-to-date info.

#### Potions in the belt

[identifying_health_potions.ipynb](docs/ocr_by_template_matching.ipynb)

To goal is to analyse the current belt, what kind of potions are available on which hotkey.

This is the next target. With some OpenCV filters and current experience it shoudl be doable.

### Interacting with the game

Using Win32 API the python app successfully sends mouse and keyboard events to the game, mocking user input. This is effectively in use to open and close the character tab with the letter 'c'.

### Understanding what is a good next step to take

Progress here is (yet) missing. At this early stage in the project the focus is solely on understanding the environment.
Q-learning, as a form of reinformcement learning, is planned to be applied to this problem.

Further resources to look into:

- [Mady - Deep Reinforcement learning](https://medium.com/deep-math-machine-learning-ai/ch-13-deep-reinforcement-learning-deep-q-learning-and-policy-gradients-towards-agi-a2a0b611617e)
- [Reinforcement Learning: An Introduction](http://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)

## Development guide

Please review `azure-pipelines.yml` for an up-to-date requirement of the environment, and steps to setup and test a fresh checkout.

## User Guide

The project only works on Microsoft Windows operating system. As Diablo is only released for Windows, this should not be an issue.

1. Obtain [Diablo](https://www.gog.com/game/diablo) from GoG
2. Checkout the repository, activate the virtual environment, install dependencies
3. Start Diablo in windowed mode. Currently the cropping expects that the window title bar is visible, do not use fullscreen-windowed mode.
4. Start the app: `python evil_snek\app.py`
5. Marvel in the beauty..

## Tooling

- [MSS](https://pypi.org/project/mss/) -> Grab the screenshot of the game, [docs here help a lot](https://python-mss.readthedocs.io/examples.html#opencv-numpy)
- [OpenCV 4.0](https://pypi.org/project/opencv-python/) -> Process the image stream
- [pywin32](https://pypi.org/project/pywin32/), WIN32 API PostMessage --> Send keyboard and mouse events to the window, simulating user input
- [Jupyter Notebook describing OCR](docs/ocr_by_template_matching.ipynb): OpenCV Template matching ( with some other image preprocessing) for Optical Character recognition (OCR).
- [Docker](https://www.docker.com/) --> for automating tests. Linux containers are used.
  
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

## Why not Tesseract

Tesseract was used as an Optical Character Recognition (OCR) engine, but was deprecated. It turned out to be very unreliable for my application, it was designed for other purposes really:

- Tesseract can identify the location of text in an image. I do not need this. The game UI is pretty static, I have a very good approximation on where the text will be.
- Off-the-shelf trained data (official or community) is not trained for [Exocet](https://fonts.adobe.com/fonts/exocet), the font of Diablo. The game mostly only uses this one font. The usual models are trained on a lot of fonts, [but not on Exocet](https://github.com/tesseract-ocr/tesseract/blob/master/src/training/language-specific.sh)
- Results were very brittle for changes in source data. Cutting the image 1-2 pixels differently ( not cutting into the important parts, doing preprocessing to eliminate background noise) created very chaotic results. It was really hard to progress in the development with confidence.
