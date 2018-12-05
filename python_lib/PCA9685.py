#!/usr/bin/python3
'''
**********************************************************************
* Filename    : PCA9685.py
* Description : A driver module for PCA9685
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Version     : v2.0.0
**********************************************************************
* Sascha Mueller zum Hagen:
* Adopted to work with the onion Omega2+ Board
**********************************************************************
'''

import time
import math
from OmegaExpansion import onionI2C

class PWM(object):
    """A PWM control class for PCA9685."""
    _MODE1              = 0x00
    _MODE2              = 0x01
    _SUBADR1            = 0x02
    _SUBADR2            = 0x03
    _SUBADR3            = 0x04
    _PRESCALE           = 0xFE
    _LED0_ON_L          = 0x06
    _LED0_ON_H          = 0x07
    _LED0_OFF_L         = 0x08
    _LED0_OFF_H         = 0x09
    _ALL_LED_ON_L       = 0xFA
    _ALL_LED_ON_H       = 0xFB
    _ALL_LED_OFF_L      = 0xFC
    _ALL_LED_OFF_H      = 0xFD

    _RESTART            = 0x80
    _SLEEP              = 0x10
    _ALLCALL            = 0x01
    _INVRT              = 0x10
    _OUTDRV             = 0x04

    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "PCA9685.py":'

    def __init__(self, address=0x5A):
        self.address = address
        self.i2c     = onionI2C.OnionI2C()

    def setup(self):
        '''Init the class with bus_number and address'''
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Reseting PCA9685 MODE1 (without SLEEP) and MODE2')
        self.write_all_value(0, 0)
        self._write_byte_data(self._MODE2, self._OUTDRV)
        self._write_byte_data(self._MODE1, self._ALLCALL)
        time.sleep(0.005)

        mode1 = self._read_byte_data(self._MODE1)
        mode1 = mode1 & ~self._SLEEP
        self._write_byte_data(self._MODE1, mode1)
        time.sleep(0.005)
        self._frequency = 60

    def _write_byte_data(self, reg, value):
        '''Write data to I2C with self.address'''
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Writing value %2X to %2X' % (value, reg))
        try:
            self.i2c.writeByte(self.address, reg, value)
        except Exception as e:
            print(e)
            self._check_i2c()

    def _read_byte_data(self, reg):
        '''Read data from I2C with self.address'''
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Reading value from %2X' % reg)
        try:
            results = self.i2c.readBytes(self.address, reg, 1)
            return results[0]
        except Exception as e:
            print(e)
            self._check_i2c()

    def _check_i2c(self):
        import commands
        bus_number = self._get_bus_number()
        print("\nYour Pi Rivision is: %s" % self._get_pi_revision())
        print("I2C bus number is: %s" % bus_number)
        print("Checking I2C device:")
        cmd = "ls /dev/i2c-%d" % bus_number
        output = commands.getoutput(cmd)
        print('Commands "%s" output:' % cmd)
        print(output)
        if '/dev/i2c-%d' % bus_number in output.split(' '):
            print("I2C device setup OK")
        else:
            print("Seems like I2C have not been set, Use 'sudo raspi-config' to set I2C")
        cmd = "i2cdetect -y %s" % self.bus_number
        output = commands.getoutput(cmd)
        print("Your PCA9685 address is set to 0x%02X" % self.address)
        print("i2cdetect output:")
        print(output)
        outputs = output.split('\n')[1:]
        addresses = []
        for tmp_addresses in outputs:
            tmp_addresses = tmp_addresses.split(':')[1]
            tmp_addresses = tmp_addresses.strip().split(' ')
            for address in tmp_addresses:
                if address != '--':
                    addresses.append(address)
        print("Conneceted i2c device:")
        if addresses == []:
            print("None")
        else:
            for address in addresses:
                print("  0x%s" % address)
        if "%02X" % self.address in addresses:
            print("Wierd, I2C device is connected, Try to run the program again, If problem stills, email this information to support@sunfounder.com")
        else:
            print("Device is missing.")
            print("Check the address or wiring of PCA9685 Server driver, or email this information to support@sunfounder.com")
        raise IOError('IO error')

    @property
    def frequency(self):
        return _frequency

    @frequency.setter
    def frequency(self, freq):
        '''Set PWM frequency'''
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Set frequency to %d' % freq)
        self._frequency = freq
        prescale_value = 25000000.0
        prescale_value /= 4096.0
        prescale_value /= float(freq)
        prescale_value -= 1.0
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Setting PWM frequency to %d Hz' % freq)
            print(self._DEBUG_INFO, 'Estimated pre-scale: %d' % prescale_value)
        prescale = math.floor(prescale_value + 0.5)
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Final pre-scale: %d' % prescale)

        old_mode = self._read_byte_data(self._MODE1);
        new_mode = (old_mode & 0x7F) | 0x10
        self._write_byte_data(self._MODE1, new_mode)
        self._write_byte_data(self._PRESCALE, int(math.floor(prescale)))
        self._write_byte_data(self._MODE1, old_mode)
        time.sleep(0.005)
        self._write_byte_data(self._MODE1, old_mode | 0x80)

    def write(self, channel, on, off):
        '''Set on and off value on specific channel'''
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Set channel "%d" to value "%d"' % (channel, off))
        self._write_byte_data(self._LED0_ON_L+4*channel, on & 0xFF)
        self._write_byte_data(self._LED0_ON_H+4*channel, on >> 8)
        self._write_byte_data(self._LED0_OFF_L+4*channel, off & 0xFF)
        self._write_byte_data(self._LED0_OFF_H+4*channel, off >> 8)

    def write_all_value(self, on, off):
        '''Set on and off value on all channel'''
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Set all channel to value "%d"' % (off))
        self._write_byte_data(self._ALL_LED_ON_L, on & 0xFF)
        self._write_byte_data(self._ALL_LED_ON_H, on >> 8)
        self._write_byte_data(self._ALL_LED_OFF_L, off & 0xFF)
        self._write_byte_data(self._ALL_LED_OFF_H, off >> 8)

    def map(self, x, in_min, in_max, out_min, out_max):
        '''To map the value from arange to another'''
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @property
    def debug(self):
        return self._DEBUG

    @debug.setter
    def debug(self, debug):
        '''Set if debug information shows'''
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print(self._DEBUG_INFO, "Set debug on")
        else:
            print(self._DEBUG_INFO, "Set debug off")

if __name__ == '__main__':
    import time

    pwm = PWM()
    pwm.frequency = 60
    for i in range(16):
        time.sleep(0.5)
        print('\nChannel %d\n' % i)
        time.sleep(0.5)
        for j in range(4096):
            pwm.write(i, 0, j)
            print('PWM value: %d' % j)
            time.sleep(0.0003)