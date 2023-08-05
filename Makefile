battery_overlay.o: main.c
	gcc main.c -o battery_overlay.o -l X11

run: battery_overlay.o
	./battery_overlay.o
