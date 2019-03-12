# Automate Diablo 1 with Python + OpenCV

[![Build Status](https://dev.azure.com/hosszub/evil_snek/_apis/build/status/hosszubalazs.evil_snek?branchName=master)](https://dev.azure.com/hosszub/evil_snek/_build/latest?definitionId=1&branchName=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=hosszubalazs_evil_snek&metric=alert_status)](https://sonarcloud.io/dashboard?id=hosszubalazs_evil_snek)

This repository is an attempt at creating a bot that plays Diablo 1. The game is only analysed from it's UI, not by direct memory access. The repository is in a super-early stage, with nothing useful in it for the moment.

This idea is heavily based on : [Python plays Grand Theft Auto V](https://www.youtube.com/watch?v=ks4MPfMq8aQ)

## User Guide

1. Obtain [Diablo](https://www.gog.com/game/diablo) from GoG
2. Checkout the repository, activate the virtual environment, install dependencies
3. Start Diablo in windowed mode in 640x480. Diablo should appear in the center of the screen.
4. Start the app: `python app.py`
5. Marvel in the beauty and uselessness of the currently available OpenCV filters

## Current state

No automation is effectilvely in place yet. Mulitple filters are applied to Diablo, as a technical proof-of-concept for OpenCV to manipulate these image streams.

The plan is to focus on a minimum viable solution for a warrior character. (probably following a very simple 1h weapon+shield strategy). As the solution matures it might be possible:

- for a single character to be dynmically ready for multiple strategies
- to make the framework moddable, making it easy to develop AI for separate classes and strategies

## Tooling

- [MSS](https://pypi.org/project/mss/) -> Grab the screenshot of the game, [docs here help a lot](https://python-mss.readthedocs.io/examples.html#opencv-numpy)
- [OpenCV 4.0](https://pypi.org/project/opencv-python/) -> Process the image stream
- [Python ctypes](https://www.google.com/search?client=firefox-b-d&q=pzthon+ctzpes), WIN32 API PostMessage --> Send keyboard and mouse events to window, simulating user input

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