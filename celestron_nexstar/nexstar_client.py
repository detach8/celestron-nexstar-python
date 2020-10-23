"""
Celestron NexStar Serial Client

https://github.com/detach8/celestron-nexstar-python

This program is distributed under the GNU General Public License v3.
See LICENSE for full license information.
"""

import math

class NexStarClient:

    # NexStar Model Codes
    MODELS = {
        1: "GPS Series",
        3: "i-Series",
        4: "i-Series SE",
        5: "CGE",
        6: "Advanced GT",
        7: "SLT",
        9: "CPC",
        10: "GT",
        11: "4/6 SE",
        12: "6/8 SE"
    }

    # NexStar Device Codes
    DEVICE_AZM_RA = b'\x10' # 16
    DEVICE_ALT_DEC = b'\x11' # 17
    DEVICE_GPS = b'\xb0' # 176
    DEVICE_RTC = b'\xb2' # 178

    def __init__(self, serial):
        self.serial = serial

    def get_location(self):
        self.serial.write(b'w')
        data = self._read(9)

        # Convert to decimal degrees
        lat = data[0] + (data[1]/60) + (data[2]/3600)
        lng = data[4] + (data[5]/60) + (data[6]/3600)

        # North/South
        if data[3] == 1:
            lat = lat * -1

        # East/West
        if data[7] == 1:
            lng = lng * -1

        return (lat, lng)

    def set_location(self, lat, lng):
        # Determine N/S E/W
        lat_ns = lat < 0
        lng_ew = lng < 0

        # Convert to DMS
        lat_abs = abs(lat)
        lng_abs = abs(lng)
        lat_d = math.trunc(lat_abs)
        lat_m = math.trunc(60 * (lat_abs - lat_d))
        lat_s = math.trunc((3600 * (lat_abs - lat_d)) - (60 * lat_m))
        lng_d = math.trunc(lng_abs)
        lng_m = math.trunc(60 * (lng_abs - lng_d))
        lng_s = math.trunc((3600 * (lng_abs - lng_d)) - (60 * lng_m))

        self.serial.write(b'W')
        self.serial.write(bytes([lat_d, lat_m, lat_s, lat_ns]))
        self.serial.write(bytes([lng_d, lng_m, lng_s, lng_ew]))

        self._read(1)

    def get_time(self):
        self.serial.write(b'h')
        data = self._read(9)

        # ISO 8601 date format
        date = str(2000 + data[5]) + '-' + str(data[3]).zfill(2) + '-' + str(data[4]).zfill(2)
        time = 'T' + str(data[0]).zfill(2) + ':' + str(data[1]).zfill(2) + ':' + str(data[2]).zfill(2)

        # Offset is a signed byte, 2's complement
        if data[6] < 128:
            offset = '+' + str(data[6]).zfill(2) + ':00'
        else:
            offset = '-' + str(256 - data[6]).zfill(2) + ':00'

        return date + time + offset

    def set_time(self, year, month, day, hour, minute, second, offset, dst):
        self.serial.write(b'H')
        self.serial.write(bytes([hour, minute, second]))
        self.serial.write(bytes([month, day, year - 2000]))

        # Offset is a signed byte, 2's complement
        if offset < 0:
            self.serial.write(bytes([offset + 256, dst]))
        else:
            self.serial.write(bytes([offset, dst]))

        self._read(1)

    def get_version(self):
        self.serial.write(b'V')
        data = self._read(3)
        return str(data[0]) + '.' + str(data[1])

    def get_device_version(self, device):
        self.serial.write(b'P\x01')
        self.serial.write(device)
        self.serial.write(b'\xfe\x00\x00\x00\x02')
        data = self._read(3)
        return str(data[0]) + '.' + str(data[1])

    def get_model(self):
        self.serial.write(b'm')
        data = self._read(2)
        return self.MODELS[data[0]]

    def is_aligned(self):
        self.serial.write(b'J')
        data = self._read(2)
        return data[0] == 1

    def is_goto_in_progress(self):
        self.serial.write(b'L')
        data = self._read(2)
        return data[0] == 49

    def cancel_goto(self):
        self.serial.write(b'M')
        data = self._read(1)

    def echo(self, i):
        self.serial.write(b'K')
        self.serial.write(bytes([i]))
        data = self._read(2)
        return data[0]

    def ping(self): 
        return self.echo(1) == 1

    def _read(self, length):
        data = self.serial.read_until(b'#')

        if (len(data) != length):
            raise Exception('Invalid response')

        return data
