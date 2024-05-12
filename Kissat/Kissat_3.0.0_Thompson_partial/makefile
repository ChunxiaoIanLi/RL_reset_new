all:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset_partial/build"
kissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset_partial/build" kissat
tissat:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset_partial/build" tissat
clean:
	rm -f "/home/ianli/MapleSATReset/KissatReset_partial"/makefile
	-$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset_partial/build" clean
	rm -rf "/home/ianli/MapleSATReset/KissatReset_partial/build"
coverage:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset_partial/build" coverage
indent:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset_partial/build" indent
test:
	$(MAKE) -C "/home/ianli/MapleSATReset/KissatReset_partial/build" test
.PHONY: all clean coverage indent kissat test tissat
