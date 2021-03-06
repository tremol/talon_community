import time

from talon import ui
from talon.voice import Context

from ..config import config
from .. import utils
from . import switcher

"""Provides a voice-driven window management application implemented in Talon.

You can use this to replace applications like Spectacle, BetterSnapTool, and Divvy.

Todo:
    - Provide for mapping keyboard shortcuts as a fallback when the new API is launched.
"""


def sorted_screens():
    """
    return screens sorted by their left most edge, from left to right
    """
    return sorted(ui.screens(), key=lambda screen: screen.visible_rect.left)


def move_screen(off=None, screen_number=None, win=None):
    if win is None:
        win = ui.active_window()

    src_screen = win.screen
    screens = sorted_screens()
    if screen_number is None:
        screen_number = (screens.index(src_screen) + off) % len(screens)
    else:
        screen_number -= 1

    dst_screen = screens[screen_number]
    if src_screen == dst_screen:
        return

    src = src_screen.visible_rect
    dst = dst_screen.visible_rect
    old = win.rect

    change_screen_mode = config.get("window_management.change_screen_mode", "same")
    if change_screen_mode == "same":
        new_rectangle = ui.Rect(
            dst.left + (old.left - src.left) / src.width * dst.width,
            dst.top + (old.top - src.top) / src.height * dst.height,
            old.width / src.width * dst.width,
            old.height / src.height * dst.height,
        )
    elif change_screen_mode == "full":
        new_rectangle = dst
    else:
        raise ValueError("{} screen mode not understood."(change_screen_mode))

    win.rect = new_rectangle
    time.sleep(0.25)
    win.rect = new_rectangle
    time.sleep(0.25)
    win.rect = new_rectangle


def resize_window(x, y, w, h):
    win = ui.active_window()
    rect = win.screen.visible_rect.copy()
    rect.x += rect.width * x
    rect.y += rect.height * y
    rect.width *= w
    rect.height *= h
    global avoid_bottom
    if avoid_bottom:
        rect.height -= 20
    win.rect = rect


def resize_to_grid(column, row, columns, rows, colspan=1, rowspan=1):
    # Ensure sane values for column and row (> 1, <= columns/rows)
    column = max(min(column, columns), 1)
    row = max(min(row, rows), 1)

    # Ensure sane values for column/row spans (e.g. if there are 3 columns, column 3 with rowspan 2 or column 2 with
    # rowspan 3 doesn't make sense). One can only span as many columns as are remaining to the right/rows downward.
    columns_remaining = columns - column
    colspan = min(max(colspan, 1), columns_remaining + 1)
    rows_remaining = rows - row
    rowspan = min(max(rowspan, 1), rows_remaining + 1)

    # Convert the grid pattern passed to the function into position and size information, then pass to resize_window().
    # We subtract 1 column/row because we need the starting position of the column, which is the ending position of the
    # previous one.
    x = (column / columns) - (1 / columns)
    y = (row / rows) - (1 / rows)

    # Width and height are just percentages. The resize function converts them to actual width/height.
    w = (1 / columns) * colspan
    h = (1 / rows) * rowspan

    resize_window(x, y, w, h)


def grid(column, row, columns, rows, colspan=1, rowspan=1):
    """Resize and move a window to a specific column and row within a grid of columns and rows. Optionally, you can
    span multiple rows or columns (to achieve things like "right two-thirds").

    Examples:
        1, 1, 2, 2: moves to top-left fourth (corner) of screen
        3, 1, 3, 1: moves to right third of screen
        3, 2, 3, 3: on a 3x3 grid, moves to the second row (out of three) on the rightmost third of the screen. In other
        words, it forms a box as tall as one-third of the screen (as that is the height of a row).
        2, 1, 3, 1, 2: right two-thirds, full height (starting at column 2 of 3, spanning two columns)
    """
    return lambda m: resize_to_grid(column, row, columns, rows, colspan, rowspan)


def next_screen(m):
    move_screen(1)


def previous_screen(m):
    move_screen(-1)


def window_move_screen(m):
    move_screen(screen_number=utils.extract_num_from_m(m))


def window_move_application_screen(m):
    move_screen(
        screen_number=utils.extract_num_from_m(m),
        win=switcher.lookup_app(m).active_window,
    )


avoid_bottom = True

# def toggle_avoid_bottom(m):
#     global avoid_bottom
#     avoid_bottom = not avoid_bottom

def avoid_bottom_on(m):
    global avoid_bottom
    avoid_bottom = True

def avoid_bottom_off(m):
    global avoid_bottom
    avoid_bottom = False

#TODO: autodetect application and apply avoid bottom or not

ctx = Context("window_management")
ctx.keymap(
    {
        # "(toggle avoid bottom | avoid bottom (on | off))": toggle_avoid_bottom,
        "avoid bottom on": avoid_bottom_on,
        "avoid bottom off": avoid_bottom_off,
        "(snap | window) left": grid(1, 1, 2, 1),
        "(snap | window) right": grid(2, 1, 2, 1),
        "snap top": grid(1, 1, 1, 2),
        "snap bottom": grid(1, 2, 1, 2),
        "snap (top | upper) left": grid(1, 1, 2, 2),
        "snap (top | upper) right": grid(2, 1, 2, 2),
        "snap (bottom | lower) left": grid(1, 2, 2, 2),
        "snap (bottom | lower) right": grid(2, 2, 2, 2),
        "(snap screen | window max)": grid(1, 1, 1, 1),
        "snap center": grid(2, 2, 8, 8, 6, 6),
        "snap next": next_screen,
        "snap last": previous_screen,
        "window next screen": next_screen,
        "window preev screen": previous_screen,
        "window [move] screen" + utils.numerals: window_move_screen,
        "[window] [move] {switcher.running} [to] screen "
        + utils.numerals: window_move_application_screen,
    }
)
