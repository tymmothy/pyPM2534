"""
PM2534.py

This module provides an API for interfacing with Philips PM2534 bench meters
via GPIB, via the Python gpib-devices package.

Copyright (c) 2011-2012, Timothy Twillman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY TIMOTHY TWILLMAN ''AS IS'' AND ANY EXPRESS
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN
NO EVENT SHALL TIMOTHY TWILLMAN OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are
those of the authors and should not be interpreted as representing official
policies, either expressed or implied, of Timothy Twillman.
"""

from gpib import generic488

class PM2534(generic488.Device488):

    """Philips PM2534 Bench Meter interface class.

    This class allows control of PM2534 bench meters over GPIB.

    Example:

        # Multimeter is set to device #22
        meter = PM2534('dev22')

        # Set function to DC voltage
        meter.function = 'VDC'

        # Set range to 3V
        meter.range = 3.0

        # Print 100 readings
        for i in xrange(0, 100):
            print meter.reading
    """

    def __init__(self, name='dev22'):
        """Create a PM2534 object.  Name is the GPIB name."""
        super(PM2534, self).__init__(name)

    def read_resp(self):
        """Read & return a response to a query command."""
        return self.read().rstrip().rsplit(' ', 1)[1]

    @property
    def id(self):
        """Get the meter's device ID string."""
        self.write('ID?')
        return self.read().rstrip()

    @property
    def function(self):
        """The current function of the meter.  Read/write string value.

        Valid values:
            VDC: DC Voltage (volts)
            VAC: AC Voltage (volts)
            RTW: Resistance (2-Wire, ohms)
            RFW: Resistance (4-Wire, ohms)
            IDC: DC Current (amps)
            IAC: AC Current (amps)
            TDC: Temperature (degrees C)
        """
        self.write('FNC ?')
        return self.read_resp()

    @function.setter
    def function(self, value):
        if not value in [ 'VDC', 'VAC', 'RTW', 'RFW', 'IDC', 'IAC', 'TDC' ]:
            raise ValueError

        self.write('FNC {:s}'.format(value))

    @property
    def range(self):
        """The meter reading range.  Read/write float or 'AUTO'.

        Note:
            Ranges are 3 * powers of 10, though the meter is smart enough
            to pick a reasonable range for most values in the ballpark.

            'AUTO' is the only valid non-numeric value.
        """
        self.write('RNG ?')
        r = self.read_resp()
        if r == 'AUTO':
            return r
        else:
            return float(r)

    @range.setter
    def range(self, value):
        if type(value) == str:
            if value.upper() == 'AUTO':
                self.write('RNG AUTO')
            else:
                raise ValueError('Unknown value for range.')
        else:
            self.write('RNG {:1.3E}'.format(value))

    @property
    def speed(self):
        """The speed of conversions.  Read/write int between 1 and 4.

        Higher conversion speeds will reduce resolution.
        """
        self.write('MSP ?')
        return int(self.read_resp())

    @speed.setter
    def speed(self, value):
        value = int(value)
        if not 1 <= value <= 4:
            raise ValueError

        self.write('MSP {:d}'.format(value))

    @property
    def resolution(self):
        """The number of digits in results.  Read/write int between 4 and 7.

        Higher resolutions will decrease conversion speed.
        """
        self.write('RSL ?')
        return int(self.read_resp())

    @resolution.setter
    def resolution(self, value):
        value = int(value)
        if not 4 <= value <= 7:
            raise ValueError

        self.write('RSL {:d}'.format(value))

    @property
    def filter(self):
        """Filtering enable control.  Read/write bool value.

        True means filtering is enabled.
        """
        self.write('FIL ?')
        s = self.read_resp()
        if s == 'ON':
            return True
        else:
            return False

    @filter.setter
    def filter(self, bool_value):
        if bool_value:
            value = 'ON'
        else:
            value = 'OFF'
        self.write('FIL {:s}'.format(value))

    @property
    def settling_time(self):
        """Internal settling time enable control.  Read/write bool value.

        True means internal settling time is enabled.
        """
        self.write('IST ?')
        s = self.read_resp()
        if s == 'ON':
            return True
        else:
            return False

    @settling_time.setter
    def settling_time(self, bool_value):
        if bool_value:
            value = 'ON'
        else:
            value = 'OFF'
        self.write('IST {:s}'.format(value))

    @property
    def display(self):
        """Display updating control.  Read/write bool value.

        When true, display updating is enabled.

        Note:
            Since display updates take some of the meter's CPU time, disabling
            the display (setting display = False) can give faster conversion
            speeds.
        """
        self.write('DSP ?')
        s = self.read_resp()
        if s == 'ON':
            return True
        else:
            return False

    @display.setter
    def display(self, bool_value):
        if bool_value:
            value = 'ON'
        else:
            value = 'OFF'
        self.write('DSP {:s}'.format(value))

    @property
    def system21_responses(self):
        """System 21 interface reception control.  Read/write bool value.

        When true, System 21 interface response reception is enabled.
        """
        self.write('AID ?')
        s = self.read_resp()
        if s == 'E':
            return True
        else:
            return False

    @system21_responses.setter
    def system21_responses(self, bool_value):
        if bool_value:
            value = 'E'
        else:
            value = 'D'
        self.write('AID {:s}'.format(value))

    @property
    def calibration(self):
        """Calibration mode control.  Read/write bool value.

        True means calibration mode is enabled.
        """
        self.write('CAL ?')
        s = self.read_resp()
        if s == 'ON':
            return True
        else:
            return False

    @calibration.setter
    def calibration(self, bool_value):
        if bool_value:
            value = 'ON'
        else:
            value = 'OFF'
        self.write('CAL {:s}'.format(value))

    @property
    def null(self):
        """NULL offset control.  Read/write bool value.

        When True, the NULL offset function is enabled.

        Note:  NULL offset is set via the store_null() function.
        """
        self.write('NUL ?')
        s = self.read_resp()
        if s == 'ON':
            return True
        else:
            return False

    @null.setter
    def null(self, bool_value):
        if bool_value:
            value = 'ON'
        else:
            value = 'OFF'
        self.write('NUL {:s}'.format(value))

    @property
    def trigger(self):
        """Meter trigger source control.  Read/write string value.

        Value is a single letter:
            I: Internal trigger
            B: IEEE Bus trigger
            E: External trigger
            K: Keyboard trigger
        """
        self.write('TRG ?')
        return self.read_resp()

    @trigger.setter
    def trigger(self, value):
        if not value in [ 'I', 'B', 'E', 'K' ]:
            raise ValueError

        self.write('TRG {:s}'.format(value))

    @property
    def text(self):
        """Display text.  Value can only be written; reading returns None.

        Note:
            To use, first turn off the display (set display=False).
        """
        return None

    @text.setter
    def text(self, value):
        self.write('TXT {:s}'.format(value))

    @property
    def reading(self):
        """Get a reading from the meter.

        Return:
            Float value; current meter reading.
        """
        return float(self.read_resp())

    def start(self):
        """Start a measurement."""
        self.write('X')

    def enter_diagnostic_mode(self):
        """Enable self diagnostic mode."""
        self.write('TST')

    def store_null(self):
        """Store the current reading as the new NULL offset."""
        self.write('NUL NEW')

