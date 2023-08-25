battery_overlay.o: battery_overlay.c images/compiled.h
	gcc battery_overlay.c -o battery_overlay.o -lX11 -lXfixes -O3 -g0

.PHONY: clean

clean:
	-rm program.o

images/compiled.h: $(wildcard images/sources/*.png)
	cd image_converter; \
		poetry run python image_converter.py --input ../images/listing.txt --output ../images/compiled.h
