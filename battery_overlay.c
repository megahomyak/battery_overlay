#include <stdio.h>
#include <stdlib.h>

#include <X11/Xlib.h>
#include <X11/extensions/shape.h>
#include <X11/extensions/Xfixes.h>

struct Context {
    Display* display;
    int screen;
    Window window;
};

struct Context build_context(void) {

}

void destroy_context() {}

#define print_error(text) fprintf(stderr, text "\n")

int main() {
    Display *display = XOpenDisplay(NULL);
    if (display == NULL) {
        print_error("Cannot open display");
        exit(1);
    }
    int screen = DefaultScreen(display);
    Window window;
    {
        enum { X = 0, Y = 0, WIDTH = 100, HEIGHT = 100, BORDER_WIDTH = 0 };
        int FOREGROUND = WhitePixel(display, screen);
        int BACKGROUND = BlackPixel(display, screen);
        window = XCreateSimpleWindow(
            display, RootWindow(display, screen), X, Y, WIDTH, HEIGHT,
            BORDER_WIDTH, BlackPixel(display, screen), WhitePixel(display, screen)
        );
    }

    struct Context context = { display, screen, window };

    /*
    Atom del_window = XInternAtom(display, "WM_DELETE_WINDOW", 0);
    XSetWMProtocols(display, window, &del_window, 1);
    */

    // Select kind of events we are interested in
    XSelectInput(display, window, ExposureMask | KeyPressMask);

    XRectangle rect;
    XserverRegion region = XFixesCreateRegion(display, &rect, 1);
    XFixesSetWindowShapeRegion(display, window, ShapeInput, 0, 0, region);
    XFixesDestroyRegion(display, region);

    // Display the window
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
