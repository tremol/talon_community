import os

from atomicwrites import atomic_write
from talon.engine import engine
from talon_init import TALON_HOME

path = os.path.join(TALON_HOME, "last_phrase")
WEBVIEW = True
NOTIFY = False
hist_len = 6


def parse_phrase(phrase):
    return " ".join(word.split("\\")[0] for word in phrase)


def on_phrase(j):
    phrase = parse_phrase(j.get("phrase", []))
    cmd = j["cmd"]
    if cmd == "p.end" and phrase:
        with atomic_write(path, overwrite=True) as f:
            f.write(phrase)


engine.register("phrase", on_phrase)
