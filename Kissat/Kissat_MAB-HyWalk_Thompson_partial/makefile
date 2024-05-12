all:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial/build"
kissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial/build" kissat
tissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial/build" tissat
clean:
	rm -f "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial"/makefile
	-$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial/build" clean
	rm -rf "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial/build"
coverage:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial/build" coverage
indent:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial/build" indent
test:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk_Thompson_partial/build" test
.PHONY: all clean coverage indent kissat test tissat
