def template2source(template: str, metadatas: dict):
    return metadatas["number"] + template[3:]


def corr(source):
    return "corr_" + source


def source2pdf(source):
    return source[:-4] + ".pdf"


def join(template):
    return source2pdf("joined" + template[3:])
