#include <stdio.h>
#include <stdlib.h>

#include <X11/Xlib.h>
#include <X11/extensions/shape.h>
#include <X11/extensions/Xfixes.h>

enum {
    RECT_X = 20,
    RECT_Y = 20,
    RECT_WIDTH = 10,
    RECT_HEIGHT = 10,

    WIN_X = 10,
    WIN_Y = 10,
    WIN_WIDTH = 100,
    WIN_HEIGHT = 100,
    WIN_BORDER = 1,
};

char a[] = {3, 5, 6};

int main() {
    /* open connection with the server */
    Display *display = XOpenDisplay(NULL);
    if (display == NULL) {
        fprintf(stderr, "Cannot open display\n");
        exit(1);
    }

    int screen = DefaultScreen(display);

    XCreateImage;

    /* create window */
    Window window = XCreateSimpleWindow(display, RootWindow(display, screen), WIN_X, WIN_Y, WIN_WIDTH, WIN_HEIGHT,
            WIN_BORDER, BlackPixel(display, screen), WhitePixel(display, screen));

    /* process window close event through event handler so XNextEvent does not fail */
    Atom del_window = XInternAtom(display, "WM_DELETE_WINDOW", 0);
    XSetWMProtocols(display, window, &del_window, 1);

    /* select kind of events we are interested in */
    XSelectInput(display, window, ExposureMask | KeyPressMask);

    XRectangle rect;
    XserverRegion region = XFixesCreateRegion(display, &rect, 1);
    XFixesSetWindowShapeRegion(display, window, ShapeInput, 0, 0, region);
    XFixesDestroyRegion(display, region);

    /* display the window */
    XMapWindow(display, window);

    /* event loop */
    XEvent event;
    while (1) {
        XNextEvent(display, &event);

        switch (event.type) {
            case KeyPress:
                /* FALLTHROUGH */
            case ClientMessage:
                goto breakout;
            case Expose:
                /* draw the window */
                // XFillRectangle(display, window, DefaultGC(display, screen), RECT_X, RECT_Y, RECT_WIDTH, RECT_HEIGHT);
                ;

                /* NO DEFAULT */
        }
    }
breakout:

    /* destroy window */
    XDestroyWindow(display, window);

    /* close connection to server */
    XCloseDisplay(display);

    return 0;
}
