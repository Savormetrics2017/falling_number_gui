# AS726x Spectral Sensor
Forked from https://github.com/pimoroni/as7262-python

Suitable for detecting the properties of ambient light, light passing through a liquid or light reflected from an object.

# Installing

Latest/development library from GitHub:

* `git clone https://github.com/HeyLlama/as726x-python`
* `cd as726x-python`
* `sudo ./install.sh`

# Example
## AS7262
```python
from as7262 import AS7262
as7262 = AS7262()
as7262.set_measurement_mode(2)
as7262.set_illumination_led(1)
```

## AS7263
```python
from as7263 import AS7263
as7263 = AS7263()
as7263.set_measurement_mode(2)
as7263.set_illumination_led(1)
```

*Note: AS7262 and AS7263 share the same I2C address. You must run these commands separately or use a MUX board*
