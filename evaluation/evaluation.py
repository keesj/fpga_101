import os

from migen import *

from migen.build.generic_platform import *
from migen.build.xilinx import XilinxPlatform

# Info
# #########################
# - Completer les questionnaire (en commentant les réponses avec #)
# - Completer le code manquant (indiqué par TODO). (Ne pas oublier la déclaration
# des submodules: self.submodules += [...])
# - Renvoyer le code completé à florent@enjoy-digital.fr

# Si migen n'est pas installé, decommenter les lignes suivantes pour installer
#os.system("rm -rf migen")
#os.system("git clone http://github.com/m-labs/migen")
#os.system("mv migen migen_tmp")
#os.system("mv migen_tmp/migen migen")
#os.system("rm -rf migen_tmp")


# Evaluation cours FPGA
# #####################

# Nom / Prenom

# 1) Décrire en quelques phrases ce qu'est un FPGA et en quoi ce type de composant
# se distingue des autres composants plus traditionnels.


# 2) Donner 3 exemples d'application où vous utiliseriez un FPGA, en expliquer les
# raisons/avantages.


# 3) Décrire les differentes étapes d'un flot de conception FPGA.


# 4) Dans un FPGA utilisant des LUT4 (4 entrées, 1 sortie)
# estimez les ressources (LUTs et Registres) des codes suivants:

# a)
#     a = Signal()
#     b = Signal()
#     c = Signal()
#     d = Signal()
#     e = Signal()
#     f = Signal()
#     g = Signal()
#     self.comb += f.eq(a & b & c & d & e)
#     self.sync += g.eq(f)

# b)
#     a = Signal(32)
#     b = Signal(32)
#     comp = Signal()
#     r = Signal()
#     self.comb += comp.eq(a == b)
#     self.sync += r.eq(comp)

# ###### NE PAS MODIFIER ######

_io = [
    ("rst", 0, Pins("C12"), IOStandard("LVCMOS33")),
    ("clk100", 0, Pins("E3"), IOStandard("LVCMOS33")),
    ("serial_tx", 0, Pins("D4"), IOStandard("LVCMOS33")),
    ("user_sw",  0, Pins("J15"), IOStandard("LVCMOS33")),
    ("user_sw",  1, Pins("L16"), IOStandard("LVCMOS33")),
    ("user_sw",  2, Pins("M13"), IOStandard("LVCMOS33")),
    ("user_sw",  3, Pins("R15"), IOStandard("LVCMOS33")),
    ("user_sw",  4, Pins("R17"), IOStandard("LVCMOS33")),
]


class Platform(XilinxPlatform):
    default_clk_name = "clk100"
    default_clk_period = 10.0

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7a100t-CSG324-1", _io, toolchain="vivado")


class Tick(Module):
    def __init__(self, sys_clk_freq, period):
        # Module's interface
        self.ce = ce = Signal() # output

        # # #

        counter_preload = int(period*sys_clk_freq - 1)
        counter = Signal(max=int(period*sys_clk_freq - 1))

        # Combinatorial assignements
        self.comb += ce.eq(counter == 0)

        # Synchronous assignments
        self.sync += \
            If(ce,
                counter.eq(counter_preload)
            ).Else(
                counter.eq(counter - 1)
            )

# ###### NE PAS MODIFIER ######

# 5) Créer un Module qui à chaque pulse sur start serialize les données sur tx.
# La première donnée est un bit de start (0), suivi de data[0], data[n], data[7]
# et d'un bit de stop (1). Pour chaque data de 8 bits, 10 bits serialisés sont donc
# transmis.
class Serializer(Module):
    """Serialize input data at 115200 bauds"""
    def __init__(self):
        # Module's interface
        self.start = start = Signal() # input
        self.data = data = Signal(8)  # input
        self.tx = tx = Signal()       # output

        # # #

        tick = Tick(100e6, 1/115200)
        self.submodules += tick

        run = Signal()
        count = Signal(4)
        self.sync += [
            # If start, set run, clear count
            # TODO
            # If tick and run, check if count != 9 and increment it if it's the
            # case / clear run it if not.
            # TODO
        ]

        # tx multiplexing
        cases = {
            0 : tx.eq(0b0), # start bit
            1 : tx.eq(data[0]),
            2 : tx.eq(0b0), # TODO
            3 : tx.eq(0b0), # TODO
            4 : tx.eq(0b0), # TODO
            5 : tx.eq(0b0), # TODO
            6 : tx.eq(0b0), # TODO
            7 : tx.eq(0b0), # TODO
            8 : tx.eq(0b0), # TODO
            9 : tx.eq(0b0)  # TODO
        }
        self.sync += If(tick.ce & run, Case(count, cases))

# ###### NE PAS MODIFIER ######

content = [
0x0a, 0x0a, 0x50, 0x6c, 0x75, 0x73, 0x20, 0x71, 
0x75, 0x27, 0x75, 0x6e, 0x65, 0x20, 0x64, 0x65, 
0x72, 0x6e, 0x69, 0x65, 0x72, 0x65, 0x20, 0x65, 
0x74, 0x61, 0x70, 0x65, 0x3a, 0x20, 0x63, 0x6f, 
0x6e, 0x6e, 0x65, 0x63, 0x74, 0x65, 0x72, 0x20, 
0x6c, 0x65, 0x73, 0x20, 0x34, 0x20, 0x70, 0x72, 
0x65, 0x6d, 0x69, 0x65, 0x72, 0x73, 0x20, 0x73, 
0x77, 0x69, 0x74, 0x63, 0x68, 0x65, 0x73, 0x20, 
0x64, 0x65, 0x20, 0x6c, 0x61, 0x20, 0x63, 0x61, 
0x72, 0x74, 0x65, 0x20, 0x61, 0x0a, 0x6c, 0x27, 
0x69, 0x6e, 0x70, 0x75, 0x74, 0x20, 0x64, 0x65, 
0x63, 0x6f, 0x64, 0x65, 0x20, 0x64, 0x65, 0x20, 
0x54, 0x72, 0x61, 0x6e, 0x73, 0x6d, 0x69, 0x74, 
0x74, 0x65, 0x72, 0x20, 0x70, 0x6f, 0x75, 0x72, 
0x20, 0x64, 0x65, 0x63, 0x6f, 0x64, 0x65, 0x72, 
0x20, 0x6c, 0x61, 0x20, 0x73, 0x65, 0x63, 0x6f, 
0x6e, 0x64, 0x65, 0x20, 0x70, 0x61, 0x72, 0x74, 
0x69, 0x65, 0x20, 0x64, 0x75, 0x20, 0x6d, 0x65, 
0x73, 0x73, 0x61, 0x67, 0x65, 0x3a, 0x0a, 0x0a, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x0f, 0x53, 
0x74, 0x67, 0x74, 0x69, 0x7e, 0x25, 0x6a, 0x7b, 
0x6a, 0x77, 0x25, 0x6b, 0x6e, 0x6c, 0x7a, 0x77, 
0x6a, 0x78, 0x25, 0x74, 0x7a, 0x79, 0x25, 0x7c, 
0x6d, 0x66, 0x79, 0x25, 0x71, 0x6e, 0x6b, 0x6a, 
0x25, 0x6e, 0x78, 0x25, 0x66, 0x71, 0x71, 0x25, 
0x66, 0x67, 0x74, 0x7a, 0x79, 0x31, 0x25, 0x66, 
0x73, 0x69, 0x25, 0x6e, 0x79, 0x25, 0x69, 0x74, 
0x6a, 0x78, 0x73, 0x2c, 0x79, 0x25, 0x72, 0x66, 
0x79, 0x79, 0x6a, 0x77, 0x33, 0x25, 0x4a, 0x7d, 
0x75, 0x71, 0x74, 0x77, 0x6a, 0x0f, 0x79, 0x6d, 
0x6a, 0x25, 0x7c, 0x74, 0x77, 0x71, 0x69, 0x33, 
0x25, 0x53, 0x6a, 0x66, 0x77, 0x71, 0x7e, 0x25, 
0x6a, 0x7b, 0x6a, 0x77, 0x7e, 0x79, 0x6d, 0x6e, 
0x73, 0x6c, 0x25, 0x6e, 0x78, 0x25, 0x77, 0x6a, 
0x66, 0x71, 0x71, 0x7e, 0x25, 0x6e, 0x73, 0x79, 
0x6a, 0x77, 0x6a, 0x78, 0x79, 0x6e, 0x73, 0x6c, 
0x25, 0x6e, 0x6b, 0x25, 0x7e, 0x74, 0x7a, 0x25, 
0x6c, 0x74, 0x25, 0x6e, 0x73, 0x79, 0x74, 0x25, 
0x6e, 0x79, 0x25, 0x69, 0x6a, 0x6a, 0x75, 0x71, 
0x7e, 0x25, 0x0f, 0x6a, 0x73, 0x74, 0x7a, 0x6c, 
0x6d, 0x33, 0x0f, 0x57, 0x6e, 0x68, 0x6d, 0x66, 
0x77, 0x69, 0x25, 0x4b, 0x6a, 0x7e, 0x73, 0x72, 
0x66, 0x73, 0x0f, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 0x28, 
0x28, 0x0f, 0x0f, 0x4a, 0x73, 0x25, 0x6a, 0x78, 
0x75, 0x6a, 0x77, 0x66, 0x73, 0x79, 0x25, 0x76, 
0x7a, 0x6a, 0x25, 0x68, 0x6a, 0x25, 0x68, 0x74, 
0x7a, 0x77, 0x78, 0x25, 0x7b, 0x74, 0x7a, 0x78, 
0x25, 0x66, 0x7a, 0x77, 0x66, 0x25, 0x69, 0x74, 
0x73, 0x73, 0x6a, 0x25, 0x76, 0x7a, 0x6a, 0x71, 
0x76, 0x7a, 0x6a, 0x78, 0x25, 0x73, 0x74, 0x79, 
0x6e, 0x74, 0x73, 0x78, 0x25, 0x69, 0x6a, 0x25, 
0x68, 0x6a, 0x25, 0x76, 0x7a, 0x6a, 0x25, 0x78, 
0x74, 0x73, 0x79, 0x25, 0x71, 0x6a, 0x78, 0x0f, 
0x4b, 0x55, 0x4c, 0x46, 0x78, 0x31, 0x25, 0x69, 
0x6a, 0x25, 0x68, 0x6a, 0x25, 0x76, 0x7a, 0x2c, 
0x6e, 0x71, 0x78, 0x25, 0x75, 0x6a, 0x77, 0x72, 
0x6a, 0x79, 0x79, 0x6a, 0x73, 0x79, 0x25, 0x69, 
0x6a, 0x25, 0x6b, 0x66, 0x6e, 0x77, 0x6a, 0x25, 
0x6a, 0x79, 0x25, 0x6a, 0x73, 0x25, 0x7b, 0x74, 
0x7a, 0x78, 0x25, 0x78, 0x74, 0x7a, 0x6d, 0x66, 
0x6e, 0x79, 0x66, 0x73, 0x79, 0x25, 0x75, 0x71, 
0x6a, 0x6e, 0x73, 0x25, 0x69, 0x6a, 0x25, 0x78, 
0x7a, 0x68, 0x68, 0x6a, 0x78, 0x0f, 0x69, 0x66, 
0x73, 0x78, 0x25, 0x7b, 0x74, 0x79, 0x77, 0x6a, 
0x25, 0x6b, 0x7a, 0x79, 0x7a, 0x77, 0x6a, 0x25, 
0x68, 0x66, 0x77, 0x77, 0x6e, 0x6a, 0x77, 0x6a, 
0x26, 0x0f, 0x4b, 0x71, 0x74, 0x77, 0x6a, 0x73, 
0x79, 0x0f]

class Transmitter(Module):
    """Send sequence of data"""
    def __init__(self):
        # Module's interface
        self.start = start = Signal() # output
        self.data = data = Signal(8)  # output

        self.decode = Signal(4)

        # # #

        lut = Memory(8, depth=len(content), init=content)
        port = lut.get_port(async_read=True)
        self.specials += lut, port

        tick = Tick(100e6, 0.005)
        self.submodules += tick

        count = Signal(max=len(content))
        self.comb += port.adr.eq(count)

        fsm = FSM(reset_state="START")
        self.submodules.fsm = fsm
        fsm.act("START",
            If(tick.ce,
                NextValue(start, 1),
                If(count >= encoder_offset,
                    NextValue(data, port.dat_r - self.decode),
                ).Else(
                    NextValue(data, port.dat_r),
                ),
                NextState("WAIT")
            )
        )
        fsm.act("WAIT",
            NextValue(start, 0),
            If(count >= (len(content) - 1),
                NextState("DONE")
            ).Else(
                NextValue(count, count + 1),
                NextState("START")
            )
        )
        fsm.act("DONE",
            NextValue(start, 0),
        )

        self.comb += port.adr.eq(count)

# ###### NE PAS MODIFIER  ######

# 6) Instancier les modules Transmitter et Serializer dans le design et les 
# connecter entre eux (start/data). Connecter la pin serial_tx à la sortie tx
# du module Serializer. Implementer le design et tester sur carte.
# Pour visualiser ce que transmet le FPGA, lancer le script:
# python3(.6) litex_term.py /dev/ttyUSBX
# Pour reseter le FPGA, appuyer sur le bouton CPU_RESET

# 7) Renseigner ci-dessous le message transmis par la carte et envoyer par mail
# ce fichier complété.

class Design(Module):
    def __init__(self, platform):
        self.submodules.crg = CRG(platform.request("clk100"), ~platform.request("rst"))

        # Transmitter
        # TODO

        # Serializer
        # TODO
        serializer = Serializer()
        self.submodules += serializer

        # Connection
        self.comb += [
        	# TODO
        ]

#
# build
#
platform = Platform()
design = Design(platform)
platform.build(design)
