from migen import *

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.uart import UARTWishboneBridge
from litex.soc.cores import dna
from litex.soc.cores.spi import SPIMaster

from ios import Led, Button, Switch
from display import Display

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

    ("user_btn", 0, Pins("P59"), IOStandard("LVCMOS33")), # JOY_RIGHT
    ("user_btn", 1, Pins("P57"), IOStandard("LVCMOS33")), # JOY_LEFT
    ("user_btn", 2, Pins("P55"), IOStandard("LVCMOS33")), # JOY_DOWN
    ("user_btn", 3, Pins("P50"), IOStandard("LVCMOS33")), # JOY_UP
    ("user_btn", 4, Pins("P47"), IOStandard("LVCMOS33")), # JOY_SELECT


    # 7 segment display
    ("display_cs_n",  0, Pins("P48 P56 P79 P85"), IOStandard("LVCMOS33")),
    ("display_abcdefg",  0, Pins("P75 P83 P66 P67 P58 P61 P81"), IOStandard("LVCMOS33")),

    ("clk32", 0, Pins("P94"), IOStandard("LVCMOS33")),

    ("cpu_reset", 0, Pins("C12"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("P105")),
        Subsignal("rx", Pins("p101")),
        IOStandard("LVCMOS33"),
    ),

    # ADC128S102 chip from National
    ("adc128s102_spi", 0,
    	Subsignal("cs_n", Pins("P88")),
        Subsignal("clk", Pins("P100")),
        Subsignal("mosi", Pins("P98")),
        Subsignal("miso", Pins("P93")),
        IOStandard("LVCMOS33")
    ),

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

def csr_map_update(csr_map, csr_peripherals):
    csr_map.update(dict((n, v)
        for v, n in enumerate(csr_peripherals, start=max(csr_map.values()) + 1)))

# create our platform (fpga interface)
platform = Platform()

# create our soc (fpga description)
class BaseSoC(SoCCore):
    # Peripherals CSR declaration
    csr_peripherals = [
        "dna",
        "leds",
        "switches",
        "buttons",
        "adc128s102",
        "display"
    ]
    csr_map_update(SoCCore.csr_map, csr_peripherals)

    def __init__(self, platform, **kwargs):
        sys_clk_freq = int(32e6)
        # SoC init (No CPU, we controlling the SoC with UART)
        SoCCore.__init__(self, platform, sys_clk_freq,
            cpu_type=None,
            csr_data_width=32,
            with_uart=False,
            with_timer=False,
            ident="My first System On Chip", ident_version=True,
        )

        # Clock Reset Generation
        self.submodules.crg = CRG(platform.request("clk32"))

        # No CPU, use Serial to control Wishbone bus
        self.add_cpu_or_bridge(UARTWishboneBridge(platform.request("serial"), sys_clk_freq, baudrate=115200))
        self.add_wb_master(self.cpu_or_bridge.wishbone)

        # FPGA identification
        self.submodules.dna = dna.DNA()

        # Led
        user_leds = Cat(*[platform.request("user_led", i) for i in range(8)])
        self.submodules.leds = Led(user_leds)

        # Switches
        user_switches = Cat(*[platform.request("user_sw", i) for i in range(8)])
        self.submodules.switches = Switch(user_switches)

        # Buttons
        user_buttons = Cat(*[platform.request("user_btn", i) for i in range(5)])
        self.submodules.buttons = Button(user_buttons)

        # Accelerometer
        self.submodules.adc128s102 = SPIMaster(platform.request("adc128s102_spi"))

        # Display
        self.submodules.display = Display(sys_clk_freq)
        self.comb += [
            platform.request("display_cs_n").eq(~self.display.cs),
            platform.request("display_abcdefg").eq(~self.display.abcdefg)
        ]


soc = BaseSoC(platform)

#
# build
#
builder = Builder(soc, output_dir="build", csr_csv="test/csr.csv")
builder.build()
