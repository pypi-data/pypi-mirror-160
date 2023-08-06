"""
Copyright © 2022  Bartłomiej Duda
License: GPL-3.0 License
"""

CRC_START_SICK = 0x0000
CRC_POLY_SICK = 0x8005


class CRC16SICKHandler:
    def __init__(self):
        self.crc16_sick_tab_calculated: bool = False
        self.crc16_sick_tab = []

    def calculate_crc16_sick(self, input_data: bytes) -> int:
        crc: int = CRC_START_SICK

        if not self.crc16_sick_tab_calculated:
            self.init_crc16_sick_tab()

        for byte in input_data:
            short_c = 0x00FF & byte
            short_p = 0

            if crc & 0x8000:
                crc = (crc << 1) ^ CRC_POLY_SICK
            else:
                crc = crc << 1

            crc ^= (short_c | short_p)
            short_p = short_c << 8

        low_byte = (crc & 0xFF00) >> 8
        high_byte = (crc & 0x00FF) << 8
        crc = low_byte | high_byte

        return crc

    def init_crc16_sick_tab(self):
        for i in range(256):
            crc = 0
            c = i
            for j in range(8):
                if (crc ^ c) & 0x0001:
                    crc = (crc >> 1) ^ CRC_POLY_SICK
                else:
                    crc = crc >> 1

                c = c >> 1

            self.crc16_sick_tab.append(crc)

        self.crc16_sick_tab_calculated = True
