from bopytex.message import Message


def activate_corr(args, deps, output):
    no_solution = args["latex"]["no_solution"]
    solution = args["latex"]["solution"]

    with open(deps[0], "r") as input_f:
        with open(output, "w") as output_f:
            for line in input_f.readlines():
                output_f.write(line.replace(no_solution, solution))

    return Message(0, [f"ACTIVATE CORR - {deps[0]} to {output}"], [])
