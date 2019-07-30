from talon import cron, ctrl
from talon.voice import Context

ctx = Context("continuous_scroll")

def scrollMe():
    global scrollAmount
    if scrollAmount:
        ctrl.mouse_scroll(by_lines=False, y=scrollAmount)


def startScrolling(rate):
    def _startScrolling(m):
        global scrollAmount, scrollJob
        scrollAmount = rate
        scrollJob = cron.interval("20ms", scrollMe)
    
    return _startScrolling

def stopScrolling(m):
    global scrollAmount, scrollJob
    scrollAmount = 0
    cron.cancel(scrollJob)

def toggle_cursor(show):
    def _toggle(_):
        global showCursor
        showCursor = show
        ctrl.cursor_visible(show)

    return _toggle

scrollAmount = 0
scrollJob = None

showCursor = True



keymap = {
    "hide cursor": toggle_cursor(False),
    "show cursor": toggle_cursor(True),
    "wheel down continuous": startScrolling(10),
    "wheel up continuous": startScrolling(-10),
    "wheel stop": stopScrolling,
}
ctx.keymap(keymap)

ctrl.cursor_visible(True)
