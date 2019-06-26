# Chalmers Signal
A sensor for civic minded data collection. Created in partnership with City of Toronto **Data Analytics and Visualization Team** and **ChalmersCards**

## Getting Started
This repository is used to support the development of the **Chalmers-Signal**. Here you'll find scripts, libraries, and neural nets we're experimenting.

### Python Virtual Environment
Most of the code in this repository is written in Python. It's reccomended that you create a *"Python Virtual Environment"* using **VirtualEnv** or your Python Virtual Environment creator of choice.

To setup your **Chalmers-Signal** python virtual environment:

**On RaspberryPi**
```bash
$ git clone https://github.com/misterchalmers/chalmers-signal-v2
$ cd chalmers-signal-v2
$ sudo ./install-dependancies
```

**On Linux Debian or Debian derivative (Mint, Ubuntu, etc.)**
```
$ sudo apt install virutalenv git python3
$ git clone https://github.com/misterchalmers/openobjecttracker
$ cd /path/to/openobjecttracker
$ virtualenv --p python3 venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```
