from jinja2.environment import Template

from bopytex.message import Message


def generate(args, deps, output):
    env = args["options"]["jinja2"]["environment"]
    template = env.get_template(deps[0])

    variables = {
        "options": args["options"],
        "subject": args["subject"],
    }

    try:
        args["options"]["direct_access"]
    except KeyError:
        pass
    else:
        for (k, v) in args["options"]["direct_access"].items():
            if k not in ["options", "subject"]:
                variables[k] = v

    try:
        with open(output, "w") as out:
            fed = template.render(variables)
            out.write(fed)

        return Message(0, [f"GENERATE - {deps[0]} to {output}"], [])

    except Exception as e:
        return Message(1, [], [e])
