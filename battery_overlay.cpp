#include <stdio.h>
#include <stdlib.h>

void die(const char *text) {
  perror(text);
  exit(-1);
}

#ifdef __linux__
int get_percentage() {
  int percentage;
  FILE *batteryFile = fopen("/sys/class/power_supply/BAT1/capacity", "r");
  if (batteryFile == NULL) {
    die("no battery file found");
  }
  if (fscanf(batteryFile, "%d", &percentage) != 1) {
    die("can't read the percentage from the battery file");
  }
  fclose(batteryFile);
  return percentage;
}
#endif
