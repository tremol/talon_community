class config:
    enabled = True
    double_click = 0.25

def toggle_enabled():
    config.enabled = not config.enabled
