import sys
import os
from as7263 import AS7263

sensor = AS7263()
sensor.set_gain(64)
sensor.set_measurement_mode(2)


class nir_sensor():
    def get_value(self):
        nir_value=[]
        r, s, t, u, v, w, count = 0, 0, 0, 0, 0, 0, 0
        for i in range(1, 10):
            values = list(sensor.get_calibrated_values())
            r += values[0]
            s += values[1]
            t += values[2]
            u += values[3]
            v += values[4]
            w += values[5]
            count += 1
        nir_value.append(round(r/count,2))
        nir_value.append(round(s/count,2))
        nir_value.append(round(t/count,2))
        nir_value.append(round(u/count,2))
        nir_value.append(round(v/count,2))
        nir_value.append(round(w/count,2))
        return nir_value