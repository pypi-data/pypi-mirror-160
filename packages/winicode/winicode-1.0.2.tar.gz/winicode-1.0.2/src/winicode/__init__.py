# -*- coding: utf-8 -*-


import os
import sys


if os.name == 'nt':
    os.system('chcp 65001 >nul 2>&1')
    if sys.stdout.encoding != 'utf8':
        sys.stdout.reconfigure(encoding='utf8')
    if sys.stderr.encoding != 'utf8':
        sys.stderr.reconfigure(encoding='utf8')
