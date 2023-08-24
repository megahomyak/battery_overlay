program.o: program.c images/images.h
	gcc program.c -o program.o -lX11 -lXfixes -O3 -g0

.PHONY: clean

clean:
	rm program.o

images/images.h: $(wildcard images/sources/*.png)
	cd image_converter; \
		poetry run python image_converter.py --output ../images/images.h --input ../images/listing.json
