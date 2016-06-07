#!/usr/bin/env python

import commands
import datetime

# How many points to measure. Make sure that you leave the baseline
# running for a significative amount before triggering the sync, it's possible
# you have significant variability in there.
POINTS = 400

SCALE = 50

commands.getoutput(
    'echo time req/s cpu mem sync_phase sync_exchange_phase '
    '> ./out/series.log')
start = datetime.datetime.now()

for i in range(POINTS):
    value = commands.getoutput('./scripts/get_ping_rate.py')
    print "Step", i, "...", value
    stats = commands.getoutput('./scripts/get_client_stats.py')
    cpu, mem, sync_phase, sync_exchange_phase = stats.split()
    sync_phase = str(int(sync_phase)*SCALE)
    sync_exchange_phase = str(int(sync_exchange_phase)*SCALE)
    now = datetime.datetime.now()
    secs = (now - start).total_seconds()
    try:
        # make it so the script exits succesfully when the server is dead
        commands.getoutput(
            'echo %s\t%s\t%s\t%s\t%s\t%s >> ./out/series.log'
            % (secs, value, cpu, mem, sync_phase, sync_exchange_phase))
    except ValueError:
        break
