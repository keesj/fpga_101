from migen import *
from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform

#
# platform
# Papilio pro with LogicStart MegaWing V1.2.1
# http://forum.gadgetfactory.net/files/file/27-logicstart-megawing-papilio-propapilio-one/

_io = [
    ("user_led",  0, Pins("P123"), IOStandard("LVCMOS33")),
    ("user_led",  1, Pins("p124"), IOStandard("LVCMOS33")),
    ("user_led",  2, Pins("P126"), IOStandard("LVCMOS33")),
    ("user_led",  3, Pins("P127"), IOStandard("LVCMOS33")),
    ("user_led",  4, Pins("P131"), IOStandard("LVCMOS33")),
    ("user_led",  5, Pins("P132"), IOStandard("LVCMOS33")),
    ("user_led",  6, Pins("P133"), IOStandard("LVCMOS33")),
    ("user_led",  7, Pins("P134"), IOStandard("LVCMOS33")),

    ("user_sw",  0, Pins("P114"), IOStandard("LVCMOS33")),
    ("user_sw",  1, Pins("P115"), IOStandard("LVCMOS33")),
    ("user_sw",  2, Pins("P116"), IOStandard("LVCMOS33")),
    ("user_sw",  3, Pins("P117"), IOStandard("LVCMOS33")),
    ("user_sw",  4, Pins("P118"), IOStandard("LVCMOS33")),
    ("user_sw",  5, Pins("P119"), IOStandard("LVCMOS33")),
    ("user_sw",  6, Pins("P120"), IOStandard("LVCMOS33")),
    ("user_sw",  7, Pins("P121"), IOStandard("LVCMOS33")),

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
class Switches(Module):
    def __init__(self, platform):     
        # synchronous assignments
        self.sync += []
        # combinatorial assignements
        for i in range(4):
            led = platform.request("user_led", i)
            sw = platform.request("user_sw", i)
            self.comb += led.eq(~sw)
        for i in range(4,8):
            led = platform.request("user_led", i)
            sw = platform.request("user_sw", i)
            self.comb += led.eq(sw)


module = Switches(platform)

#
# build
#

platform.build(module)
