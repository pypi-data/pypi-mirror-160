import subprocess

from bopytex.message import Message

from ..message import SubprocessMessage


def curstomtex(command: str, options: str):
    def func(args: dict, deps, output) -> Message:
        compile_process = subprocess.Popen(
            [command, options, deps[0]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        return Message(
            compile_process.wait(),
            list(compile_process.stdout),
            list(compile_process.stderr),
        )

    return func


latexmk = curstomtex("latexmk", "-f")
pdflatex = curstomtex("pdflatex", "--interaction=nonstopmode")
