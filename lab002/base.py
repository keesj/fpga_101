from migen import *
from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform
from migen.genlib.cdc import MultiReg

from tick import *
from display import *
from bcd import *
from core import *


#
# platform
#

_io = [
    # Led on board
    ("user_led",  0, Pins("P112"), IOStandard("LVCMOS33")),

    # Logic Start MegaWing JOY SELECT
    ("user_sw",  0, Pins("P47"), IOStandard("LVCMOS33")),

    # JOY RIGHT AND LEFT
    ("user_btn_r", 0, Pins("P59"), IOStandard("LVCMOS33")),
    ("user_btn_l", 0, Pins("P57"), IOStandard("LVCMOS33")),

    ("clk32", 0, Pins("P94"), IOStandard("LVCMOS33")),

    # 7 segment display
    ("display_cs_n",  0, Pins("P85 P79 P56 P48"), IOStandard("LVCMOS33")),
    ("display_abcdefg",  0, Pins("P75 P83 P66 P67 P58 P61 P81 P51"), IOStandard("LVCMOS33")),
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

# user button detection
class UserButtonPress(Module):
    def __init__(self, user_btn):
        self.rising = Signal()

        # # #

        _user_btn = Signal()
        _user_btn_d = Signal()

        # resynchronize user_btn
        self.specials += MultiReg(user_btn, _user_btn)
        # detect rising edge
        self.sync += [
            _user_btn_d.eq(user_btn),
            self.rising.eq(_user_btn & ~_user_btn_d)
        ]

# create our platform (fpga interface)
platform = Platform()

# create our main module (fpga description)
class Clock(Module):
    sys_clk_freq = int(32e6)
    def __init__(self):
        # -- TO BE COMPLETED --
        # Tick generation : timebase

        # Display

        # Core : counts ss/mm/hh

        # set mm/hh

        # Binary Coded Decimal: convert ss/mm/hh to decimal values

        # use the generated verilog file
    
        # combinatorial assignement
        self.comb += [
            # Connect tick to core (core timebase)

            # Set minutes/hours

            # Convert core seconds to bcd and connect
            # to display

            # Convert core minutes to bcd and connect
            # to display

            # Convert core hours to bcd and connect
            # to display

            # Connect display to pads
        ]
        # -- TO BE COMPLETED --

module = Clock()

#
# build
#

platform.build(module)
