from migen import *
from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform
from migen.genlib.cdc import MultiReg

from tick import *
from display import Display as Dis
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
    ("display_abcdefg",  0, Pins("P75 P83 P66 P67 P58 P61 P81"), IOStandard("LVCMOS33")),
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
        tick = Tick(self.sys_clk_freq,1)
        self.submodules += tick

        # Display
        disp = Dis(self.sys_clk_freq)
        self.submodules += disp
        # Core : counts ss/mm/hh
        core = CoreDus()
        self.submodules += core
        #c.
        # set mm/hh
        btn0_press = UserButtonPress(platform.request("user_btn_r"))
        btn1_press = UserButtonPress(platform.request("user_btn_l"))
        btn2_press = UserButtonPress(platform.request("user_sw"))
        self.submodules += btn0_press, btn1_press, btn2_press

        # set mm/hh
        bcd_seconds = BCD()
        bcd_minutes = BCD()

        self.submodules += bcd_seconds,bcd_minutes

        # Binary Coded Decimal: convert ss/mm/hh to decimal values

        # use the generated verilog file
    
        # combinatorial assignement
        self.comb += [
            # Connect tick to core (core timebase)
            core.tick.eq(tick.ce),
            core.inc_minutes.eq(btn1_press.rising),
            core.reset_time.eq(btn2_press.rising),

            # Set minutes/hours
            bcd_seconds.value.eq(core.seconds),
            disp.values[3].eq(bcd_seconds.ones),
            disp.values[2].eq(bcd_seconds.tens),
            
            # Convert core seconds to bcd and connect
            # to display
            bcd_minutes.value.eq(core.minutes),
            disp.values[0].eq(bcd_minutes.tens),
            disp.values[1].eq(bcd_minutes.ones),
            #disp.values[2].eq(0x3),
            #disp.values[3].eq(0x4),
            # Convert core minutes to bcd and connect
            # to display

            # Convert core hours to bcd and connect
            # to display

            # Connect display to pads
            platform.request("display_cs_n").eq(~disp.cs),
            platform.request("display_abcdefg").eq(~disp.abcdefg)
        ]
        # -- TO BE COMPLETED --

module = Clock()

#
# build
#
def base_test(dut):
        for i in range(10240):
                yield	

platform.build(module)
#run_simulation(module,base_test(module),vcd_name="base.vcd")
