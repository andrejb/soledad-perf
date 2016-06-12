# Actual soledad sync

soledad-sync-server:
	twistd -n web --port 8080 --class=scripts.server_with_soledad_syncer.resource

soledad-sync-server-lineprof:
	kernprof -l ./scripts/server_with_soledad_syncer.py


soledad-sync-server-debug:
	#twistd --profile=stats_obj --profiler=cProfile -n web --port 8080 --class=server_with_soledad_syncer.resource
	python -m cProfile -o sync.cprofile ./scripts/server_with_soledad_syncer.py 

view-lineprofile:
	python -m line_profiler ./scripts/server_with_soledad_syncer.py.lprof


view-profile:
	cprofilev -f sync.cprofile

measure-ping:
	httperf --server localhost --port 8080 --num-calls 5 --num-conns 20 --uri /ping

trigger-create-docs:
	curl localhost:8080/create-docs

trigger-sync:
	curl localhost:8080/start-sync

trigger-stop:
	curl localhost:8080/stop

measure-series:
	# TODO make sure we have restarted the server, send SIGNUP ?
	# TODO rm series.log, name it with a timestamp
	# TODO measure, first of all, the number of seconds from the beginning!!! (right now it's biased)
	# TODO add cpu/ram usage (ping command COULD RETURN THAT!)
	#rm -f /tmp/soledadsync/*
	rm -f ./out/series.log
	./scripts/measure_perf_series.py

graph-image:
	gnuplot -e 'call "./scripts/sync_stats.gnuplot" "./out/series.log" "./out/sync-stats.png"'

graph-view:
	gnuplot -e 'call "./scripts/sync_stats.gnuplot" "./out/series.log" ""'

kill:
	killall -9 twistd
	killall -9 python
