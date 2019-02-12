from migen import *
from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform

#
# platform
#

_io = [
    ("user_led",  0, Pins("P123"), IOStandard("LVCMOS33")),
    ("user_led",  1, Pins("p124"), IOStandard("LVCMOS33")),
    ("user_led",  2, Pins("P126"), IOStandard("LVCMOS33")),
    ("user_led",  3, Pins("P127"), IOStandard("LVCMOS33")),
    ("user_led",  4, Pins("P131"), IOStandard("LVCMOS33")),
    ("user_led",  5, Pins("P132"), IOStandard("LVCMOS33")),
    ("user_led",  6, Pins("P133"), IOStandard("LVCMOS33")),
    ("user_led",  7, Pins("P134"), IOStandard("LVCMOS33")),

    ("clk32", 0, Pins("P94"), IOStandard("LVCMOS33")),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk32"
    default_clk_period = 31.25

    def __init__(self):
        XilinxPlatform.__init__(self, "xc6slx9-tqg144-2", _io)

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)

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


class RGBBlink(Module):
    def __init__(self,platform):
        # sub modules
        led_a = Blink(1, 32e6, platform.request("user_led",0))
        led_b = Blink(2, 32e6, platform.request("user_led",1))
        led_c = Blink(4, 32e6, platform.request("user_led",2))
        self.submodules += led_a, led_b, led_c

module = RGBBlink(platform)
#
# build
#

platform.build(module)
