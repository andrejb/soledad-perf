#!/usr/bin/env python

"""
Get stats from dummy server running Soledad Client and spit them out.
"""

import commands
import urllib

stats = urllib.urlopen('http://localhost:8080/stats').read().split()

pid, sync_phase, sync_exchange_phase = stats

res = commands.getoutput("ps -p " + pid + " -o \%cpu,\%mem")
splitted = res.split()
cpu = splitted[2]
mem = splitted[3]

print cpu, mem, sync_phase, sync_exchange_phase
