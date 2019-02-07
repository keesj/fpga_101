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

# create our module (fpga description)
class Blink(Module):
    def __init__(self, blink_freq, sys_clk_freq, led):
        counter = Signal(32)     
        # synchronous assignments
        self.sync += [
            counter.eq(counter + 1),
            If(counter == int((sys_clk_freq/blink_freq)/2 - 1),
                counter.eq(0),
                led.eq(~led)
            )
        ]
        # combinatorial assignements
        self.comb += []

module = Blink(1, 16e6, platform.request("user_led"))

#
# build
#

platform.build(module)
