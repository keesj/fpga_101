#!/usr/bin/env python3
import os
# The papilio pro comes with an ide and a fork of xc3sprog called papilio_prog
# https://github.com/GadgetFactory/Papilio-Loader/tree/master/xc3sprog/trunk/bscan_spi
#
#
# xc3sprog was cloned from https://github.com/matrix-io/xc3sprog.git
# patched with 858454a04ba8cf87125982beca666286b9f63362 ([PATCH] fix WiringPI API dependency)
# 
os.system("xc3sprog -v -c papilio build/top.bit")
