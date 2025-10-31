import curses
import plotting
import util
def main(stdscr):

    curses.start_color()
    # Clear screen
    util.clear()
    stdscr.clear()

    delayTime = 50  # Delay for each line bein printed in milliseconds
    # Print Hello World in the center of the screen
    height, width = stdscr.getmaxyx()
    # Call the plot_stock function to display a stock chart
    plot = plotting.plot_stock("AAPL", period="1y", interval="1d")
    lines = plot.split("\n")

    #Prints each line in the graph with a delay
    for i, line in enumerate(lines):
        curses.delay_output(delayTime)
        if 0 <= i < height - 1:  # prevent writing off-screen
            try:
                stdscr.addstr(i, 2, line[:width-2])  # clip long lines
            except curses.error:
                pass
        stdscr.refresh()
    # Refresh to show the changes
    # Wait for user input before exiting
    stdscr.getch()

curses.wrapper(main)