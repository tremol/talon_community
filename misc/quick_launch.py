import subprocess

from talon.voice import Context


def new_research_note(m):
    """ Start a new LaTeX note in folder """
    folder = "/Users/priggins/Dropbox/Berkeley-current/Research/mixed_notes3/"
    timestamp = subprocess.check_output(["date", "+%m-%d-%y_%H-%M"]).decode('utf-8')
    timestamp = timestamp[:-1] # strip off trailing newline
    subprocess.run(["/bin/cp",
                    folder + "notes_template.tex",
                    folder + "researchNote_" + timestamp + ".tex"])
    subprocess.run(["/usr/local/bin/atom",
                    "-n",
                    folder + "researchNote_" + timestamp + ".tex"])

ctx = Context("quick_launch")

ctx.keymap(
    {
        'start a new note': new_research_note,
    }
)
