#!/usr/bin/env python3
from migen import *
from migen.build.generic_platform import *
from migen.build.lattice import LatticePlatform

#
# platform
#

_io = [
    ("user_led", 0, Pins("B3"), IOStandard("LVCMOS33")),
    ("clk16", 0, Pins("B2"), IOStandard("LVCMOS33")),
]


class Platform(LatticePlatform):
    default_clk_name = "clk16"
    default_clk_period = 62.5

    def __init__(self):
        LatticePlatform.__init__(self, "ice40-lp8k-cm81", _io,
                                 toolchain="icestorm")

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)

#
# design
#


# create our platform (fpga interface)
platform = Platform()
led = platform.request("user_led")

# create our module (fpga description)
module = Module()

# create a counter and blink a led
counter = Signal(26)
module.comb += led.eq(counter[25])
module.sync += counter.eq(counter + 1)

#
# build
#

platform.build(module)
