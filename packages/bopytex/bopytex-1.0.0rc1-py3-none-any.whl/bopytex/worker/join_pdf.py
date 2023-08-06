import subprocess

from bopytex.message import Message, SubprocessMessage


def pdfjam(args: dict, deps, output):
    joining_process = subprocess.Popen(
        ["pdfjam"] + deps + ["-o", output],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return Message(
        joining_process.wait(),
        list(joining_process.stdout),
        list(joining_process.stderr),
    )


def gs(args: dict, deps, output):
    """Not working. The command works in terminal but not here"""
    joining_process = subprocess.Popen(
        ["gs", f"-dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile={output}"] + deps,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    return Message(
        joining_process.wait(),
        list(joining_process.stdout),
        list(joining_process.stderr),
    )
