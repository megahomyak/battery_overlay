program.o: program.c battery.h
	gcc program.c -o program.o -lX11 -lXfixes -O3 -g0

.PHONY: clean

clean:
	rm program.o

images/converted/%.h: images/source/%.png
	cd image_converter
	poetry run python image_converter.py --output ../$@ --input ../$< --variable-name $(*F)
