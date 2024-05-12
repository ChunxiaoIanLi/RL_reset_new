all:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson/build"
kissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson/build" kissat
tissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson/build" tissat
clean:
	rm -f "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson"/makefile
	-$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson/build" clean
	rm -rf "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson/build"
coverage:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson/build" coverage
indent:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson/build" indent
test:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson/build" test
.PHONY: all clean coverage indent kissat test tissat
