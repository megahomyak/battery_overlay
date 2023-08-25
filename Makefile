program.o: program.c images/compiled.h
	gcc program.c -o program.o -lX11 -lXfixes -O3 -g0

.PHONY: clean

clean:
	-rm program.o

images/compiled.h: $(wildcard images/sources/*.png)
	cd image_converter; \
		poetry run python image_converter.py --path ../images
