#!/usr/bin/env python3

import importlib
import sys
rc = 0

for sdr in ("AirSpy", "BladeRF", "HackRF", "RTLSDR", "LimeSDR", "PlutoSDR", "SDRPlay", "USRP"):
    try:
        importlib.import_module(f'.{sdr.lower()}', 'urh.dev.native.lib')
        print("{:<10} \033[92mSUCCESS\033[0m".format(f"{sdr}:"))
    except ImportError as e:
        print("{:<10} \033[91mFAILURE\033[0m ({})".format(f"{sdr}:", e))
        rc = 1

sys.exit(rc)
