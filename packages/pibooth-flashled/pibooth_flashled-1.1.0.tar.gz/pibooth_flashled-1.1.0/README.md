pibooth-flashled
=================

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-red.svg)](https://www.python.org/downloads)
[![PyPi package](https://badge.fury.io/py/pibooth-flashled.svg)](https://pypi.org/project/pibooth-flashled)
[![PyPi downloads](https://img.shields.io/pypi/dm/pibooth-flashled?color=purple)](https://pypi.org/project/pibooth-flashled)

`pibooth-flashled` is a plugin for the [pibooth](https://pypi.org/project/pibooth) application.

It adds a flash with warm white and cold white when the capture is taken.

Install
-------

```
pip3 install pibooth-flashled
    
sudo systemctl enable pigpiod
sudo systemctl start pigpiod 
```
    

Configuration
-------------

Below are the new configuration options available in the [pibooth](https://pypi.org/project/pibooth) configuration. **The keys and their default values are automatically added to your configuration after first** [pibooth](https://pypi.org/project/pibooth) **restart.**

``` {.ini}
[FLASH]

# Physical GPIO OUT pin to light a warm white LED strip
warmwhite_pin = 12
    
# Physical GPIO OUT pin to light a cool white LED strip
coolwhite_pin = 13
		
# The white balance (warm white, cool white) in percent
white_balance = (50, 50)

# The brightness in percent
brightness = 50
		
# How long is the fade light in milliseconds (0 to skip it)
fade_delay = 1000

```

### Note

Edit the configuration by running the command `pibooth --config`.

