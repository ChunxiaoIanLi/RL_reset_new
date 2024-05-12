all:
	$(MAKE) -C "/home/z52lu/MapleSATReset/KissatReset/build"
kissat:
	$(MAKE) -C "/home/z52lu/MapleSATReset/KissatReset/build" kissat
tissat:
	$(MAKE) -C "/home/z52lu/MapleSATReset/KissatReset/build" tissat
clean:
	rm -f "/home/z52lu/MapleSATReset/KissatReset"/makefile
	-$(MAKE) -C "/home/z52lu/MapleSATReset/KissatReset/build" clean
	rm -rf "/home/z52lu/MapleSATReset/KissatReset/build"
coverage:
	$(MAKE) -C "/home/z52lu/MapleSATReset/KissatReset/build" coverage
indent:
	$(MAKE) -C "/home/z52lu/MapleSATReset/KissatReset/build" indent
test:
	$(MAKE) -C "/home/z52lu/MapleSATReset/KissatReset/build" test
.PHONY: all clean coverage indent kissat test tissat
