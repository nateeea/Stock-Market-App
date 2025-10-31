import curses
import plotting
import data
import time
import util
def main(stdscr):

    curses.start_color()
    # define color pairs for percent change (green positive, red negative) and labels
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
    # Clear screen
    util.clear()
    stdscr.clear()
    stdscr.refresh()
    
    # Use fixed-size variables for layout (not relative to terminal size)
    # Adjust these constants to control the exact box sizes
    INFO_H = 3
    # Keep the graph size fixed and derive the info box sizes from it
    GRAPH_H = 20
    GRAPH_W = 75  # fixed graph width
    # Derive info box widths from GRAPH_W but allow wrapping to multiple rows
    delayTime = 40  # Delay for each line being printed in milliseconds
    # Call the plot_stock function to get the chart and metrics
    symbol = "BTC-USD"
    plot, start_price, price, pct_change, period = plotting.plot_stock(symbol, period="6mo", interval="1d")
    lines = plot.split("\n")

    # Build content strings for the info boxes
    def make_contents(price_val, pct_val):
        return [f"Ticker: {symbol}", f"Price: ${price_val:,.2f}", f"Change: {pct_val:+.2f}%", f"Period: {period}"]

    contents = make_contents(price, pct_change)

    def compute_positions(contents):
        # minimal width for a box (including padding/borders)
        min_w = 12
        needed = [max(min_w, len(s) + 4) for s in contents]
        rows = []
        cur_row = []
        cur_sum = 0
        for w in needed:
            if cur_row and cur_sum + w > GRAPH_W:
                rows.append(cur_row)
                cur_row = [w]
                cur_sum = w
            else:
                cur_row.append(w)
                cur_sum += w
        if cur_row:
            rows.append(cur_row)

        # positions: list of tuples (row_i, x, width, content_index)
        positions = []
        idx = 0
        for row_i, row in enumerate(rows):
            x = 0
            for w in row:
                positions.append((row_i, x, w, idx))
                x += w
                idx += 1
        return positions, len(rows)

    positions, rows_count = compute_positions(contents)

    # Ensure terminal is large enough for our computed layout
    term_h, term_w = stdscr.getmaxyx()
    required_h = rows_count * INFO_H + GRAPH_H
    required_w = GRAPH_W
    if term_h < required_h or term_w < required_w:
        stdscr.addstr(0, 0, f"Terminal too small: need {required_w}x{required_h} (WxH). Resize and retry. Press any key to exit.")
        stdscr.refresh()
        stdscr.getch()
        return

    # Create info windows according to computed positions
    info_windows = [None] * len(contents)
    for row_i, x, w, idx in positions:
        y = row_i * INFO_H
        win = curses.newwin(INFO_H, w, y, x)
        win.box()
        info_windows[idx] = win

    # graphWin placed below the info rows
    graph_y = rows_count * INFO_H
    graphWin = curses.newwin(GRAPH_H, GRAPH_W, graph_y, 0)
    graphWin.box()

    # Helper: draw info windows and graph
    def draw_all(current_price, current_pct, lines):
        contents = make_contents(current_price, current_pct)
        # draw info boxes
        for idx, text in enumerate(contents):
            try:
                w = info_windows[idx]
                w.erase()
                w.box()
                if idx == 0:
                    w.addstr(1, 2, text, curses.color_pair(3))
                elif idx == 2:
                    color = curses.color_pair(1) if current_pct >= 0 else curses.color_pair(2)
                    w.addstr(1, 2, text, color)
                else:
                    w.addstr(1, 2, text)
                w.refresh()
            except (curses.error, TypeError):
                pass

        # draw graph
        graphWin.erase()
        graphWin.box()
        for i, line in enumerate(lines):
            if 0 <= i < GRAPH_H - 2:
                try:
                    graphWin.addstr(i+1, 1, line[:GRAPH_W-2])
                except curses.error:
                    pass
        graphWin.refresh()

    # Initial draw
    draw_all(price, pct_change, lines)

    # Now enter an update loop: poll for latest price every 5 seconds and update boxes
    stdscr.nodelay(True)
    UPDATE_INTERVAL = 5.0
    last_update = time.time()
    try:
        while True:
            ch = stdscr.getch()
            if ch != -1:
                # any key pressed -> exit
                break

            now = time.time()
            if now - last_update >= UPDATE_INTERVAL:
                new_price = data.get_latest_price(symbol)
                if new_price is not None:
                    price = new_price
                    # Recompute percent change using the period start price
                    pct_change = ((price / start_price) - 1.0) * 100 if start_price != 0 else 0.0

                    # Build new contents and check if any box needs more width than current
                    new_contents = make_contents(price, pct_change)
                    needs_relayout = False
                    for idx, text in enumerate(new_contents):
                        needed_w = max(12, len(text) + 4)
                        try:
                            cur_w = info_windows[idx].getmaxyx()[1]
                        except Exception:
                            cur_w = 0
                        if needed_w > cur_w:
                            needs_relayout = True
                            break

                    if needs_relayout:
                        # Recompute positions and recreate windows
                        positions, rows_count = compute_positions(new_contents)
                        # check terminal size
                        term_h, term_w = stdscr.getmaxyx()
                        required_h = rows_count * INFO_H + GRAPH_H
                        required_w = GRAPH_W
                        if term_h < required_h or term_w < required_w:
                            # can't relayout due to terminal size; skip update
                            last_update = now
                            continue

                        # create new windows
                        info_windows = [None] * len(new_contents)
                        for row_i, x, w, idx in positions:
                            y = row_i * INFO_H
                            win = curses.newwin(INFO_H, w, y, x)
                            win.box()
                            info_windows[idx] = win

                        # recreate graph window below new rows
                        graph_y = rows_count * INFO_H
                        graphWin = curses.newwin(GRAPH_H, GRAPH_W, graph_y, 0)
                        graphWin.box()

                        # redraw everything
                        draw_all(price, pct_change, lines)
                    else:
                        # simple redraw into existing windows
                        draw_all(price, pct_change, lines)

                last_update = now

            time.sleep(0.1)
    finally:
        # restore blocking getch behavior
        stdscr.nodelay(False)

curses.wrapper(main)