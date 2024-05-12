all:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk/build"
kissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk/build" kissat
tissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk/build" tissat
clean:
	rm -f "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk"/makefile
	-$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk/build" clean
	rm -rf "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk/build"
coverage:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk/build" coverage
indent:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk/build" indent
test:
	$(MAKE) -C "/home/ianli/MapleSATReset/Kissat_MAB-HyWalk/build" test
.PHONY: all clean coverage indent kissat test tissat
