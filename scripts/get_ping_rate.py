#!/usr/bin/env python

"""
Measure the connection rate to the dummy server running Soledad Client using
httperf and spit it out.
"""

import commands
import re

res = commands.getoutput(
    'httperf --server localhost --port 8080 --num-calls 5 --num-conns 10 '
    '--uri /ping  | grep "Connection rate"')
print re.findall('[-+]?([0-9]*\.?[0-9]+)', res)[0]
