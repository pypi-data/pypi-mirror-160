from bopytex.jinja2_env.texenv import texenv
from bopytex.planner.generate_compile_join_planner import planner
from bopytex.worker import Dispatcher
from bopytex.worker.activate_corr import activate_corr
from bopytex.worker.clean import clean
from bopytex.worker.compile import pdflatex
from bopytex.worker.generate import generate
from bopytex.worker.join_pdf import pdfjam

jinja2 = {"environment": texenv}

dispatcher = Dispatcher(
    {
        "GENERATE": generate,
        "COMPILE": pdflatex,
        "JOIN": pdfjam,
        "CLEAN": clean,
        "ACTIVATE_CORR": activate_corr,
    }
)

latex = {
    "solution": r"solution/print = true",
    "no_solution": r"solution/print = false",
}
