battery_overlay.o: main.cpp
	gcc main.cpp -o battery_overlay.o

run: battery_overlay.o
	./battery_overlay.o
