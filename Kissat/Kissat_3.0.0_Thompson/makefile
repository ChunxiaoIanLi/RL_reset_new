all:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset/build"
kissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset/build" kissat
tissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset/build" tissat
clean:
	rm -f "/home/ianli/MapleSATReset/KissatReset"/makefile
	-$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset/build" clean
	rm -rf "/home/ianli/MapleSATReset/KissatReset/build"
coverage:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset/build" coverage
indent:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset/build" indent
test:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset/build" test
.PHONY: all clean coverage indent kissat test tissat
