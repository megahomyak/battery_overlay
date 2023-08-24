program.o: program.c battery.h
	gcc program.c -o program.o -lX11 -lXfixes -O3 -g0

.PHONY: clean

clean:
	rm program.o

battery.h: battery.png
	python image_converter.py battery
