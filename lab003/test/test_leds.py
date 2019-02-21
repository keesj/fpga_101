#!/usr/bin/env python3

import time
import random

from litex.soc.tools.remote import RemoteClient

wb = RemoteClient()
wb.open()

# # #

# test led
print("Testing Led...")
for i in range(0xff +1):
    wb.regs.leds_out.write(i)
    time.sleep(0.1)


# # #

wb.close()
