import os

import bopytex.planner.naming as naming
from bopytex.tasks import Task, activate_corr_on, compile_pdf, join_pdfs


def list_files(dir=".", accept=lambda _: True, reject=lambda _: False):
    files = []
    for file in os.listdir(dir):
        if accept(file) and not reject(file):
            files.append(file)
    return files


def planner(options: dict) -> list[Task]:
    sources = list_files(
        accept=lambda x: x.endswith(".tex"),
        reject=lambda x: x.startswith("tpl_"),
    )
    options["sources"] = sources
    return tasks_builder(options)


def tasks_builder(
    options: dict,
) -> list[Task]:
    opt = {
        "no_join": False,
        "no_pdf": False,
    }
    opt.update(options)

    try:
        sources = opt["sources"]
        no_join = opt["no_join"]
        no_pdf = opt["no_pdf"]
    except KeyError:
        raise PlannerMissingOption("An option is missing")

    tasks = []
    corr_pdfs = []

    for source in sources:
        corr_source = naming.corr(source)
        tasks.append(activate_corr_on(source, opt, corr_source))

        if not no_pdf:
            corr_pdf = naming.source2pdf(corr_source)
            tasks.append(compile_pdf(corr_source, corr_pdf))
            corr_pdfs.append(corr_pdf)

    if not no_join:
        joined = "joined.pdf"

        if corr_pdfs:
            corr_joined = naming.corr(joined)
            tasks.append(join_pdfs(corr_pdfs, corr_joined))

    return tasks
