"""Library for the AS7263 Visble Light Spectral Sensor."""
import as7263

if __name__ == '__main__':
    as7263.soft_reset()

    hw_type, hw_version, fw_version = as7263.get_version()

    print('{}'.format(fw_version))

    as7263.set_gain(64)

    as7263.set_integration_time(17.857)

    as7263.set_measurement_mode(2)

    # as7262.set_illumination_led_current(12.5)
    as7263.set_illumination_led(1)
    # as7262.set_indicator_led_current(2)
    # as7262.set_indicator_led(1)

    try:
        while True:
            values = as7263.get_calibrated_values()
            print("""
610nm:    {}
680nm: {}
730nm: {}
760nm:  {}
810nm:   {}
860nm: {}""".format(*values))
    except KeyboardInterrupt:
        as7263.set_measurement_mode(3)
        as7263.set_illumination_led(0)
