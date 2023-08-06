import csv

import bopytex.planner.naming as naming
from bopytex.planner.exceptions import PlannerMissingOption
from bopytex.tasks import Task, activate_corr_on, compile_pdf, generate, join_pdfs


def build_subject_list_from_infos(infos: list[dict]) -> list[dict]:
    subjects = []
    digit = len(str(len(infos)))
    for i, infos in enumerate(infos):
        subjects.append({"number": str(i + 1).zfill(digit), **infos})
    return subjects


def build_subject_list_from_qty(qty: int) -> list[dict]:
    subjects = []
    digit = len(str(qty))
    for i in range(qty):
        subjects.append({"number": str(i + 1).zfill(digit)})
    return subjects


def planner(options: dict) -> list[Task]:
    try:
        students_csv = options["students_csv"]
        assert options["students_csv"] != ""

    except (KeyError, AssertionError):
        try:
            quantity_subjects = options["quantity_subjects"]
            assert options["quantity_subjects"] != 0
        except (KeyError, AssertionError):
            raise PlannerMissingOption("students_csv or quantity_subjects is required")
        else:
            options["subjects"] = build_subject_list_from_qty(qty=quantity_subjects)

    else:
        with open(students_csv, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            infos = [r for r in reader]
        options["subjects"] = build_subject_list_from_infos(infos)

    return tasks_builder(options)


def tasks_builder(
    options: dict,
) -> list[Task]:

    opt = {
        "corr": False,
        "no_join": False,
        "no_pdf": False,
    }
    opt.update(options)

    try:
        template = opt["template"]
        subjects = opt["subjects"]
        corr = opt["corr"]
        no_join = opt["no_join"]
        no_pdf = opt["no_pdf"]
    except KeyError:
        raise PlannerMissingOption("An option is missing")

    tasks = []

    pdfs = []
    corr_pdfs = []

    for subject in subjects:
        source = naming.template2source(template, subject)
        args = {"subject": subject, "options": options}

        tasks.append(generate(template, args, source))

        if not no_pdf:
            pdf = naming.source2pdf(source)
            tasks.append(compile_pdf(source, pdf))
            pdfs.append(pdf)

        if corr:
            corr_source = naming.corr(source)
            tasks.append(activate_corr_on(source, opt, corr_source))

            if not no_pdf:
                corr_pdf = naming.source2pdf(corr_source)
                tasks.append(compile_pdf(corr_source, corr_pdf))
                corr_pdfs.append(corr_pdf)

    if not no_join:
        joined = naming.join(template)
        if pdfs:
            tasks.append(join_pdfs(pdfs, joined))

        if corr_pdfs:
            corr_joined = naming.corr(joined)
            tasks.append(join_pdfs(corr_pdfs, corr_joined))

    return tasks
