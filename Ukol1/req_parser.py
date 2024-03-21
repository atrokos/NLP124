from typing import Optional



def tokenize_command(comm: str) -> list[str]:
    result = []
    curr = []

    for char in comm.strip():
        match char:
            case "(" | ")":
                if len(curr) > 0:
                    result.append("".join(curr))
                    curr = []
                result.append(char)
            case " ":
                if len(curr) > 0:
                    result.append("".join(curr))
                    curr = []
            case _:
                curr.append(char)

    if len(curr) > 0:
        result.append("".join(curr))

    return result

# -> tuple[dict[str, dict[str, str]], list[str]]
def parse_command(tokens: list[str]):
    operands = []
    operators = []
    for i in range(len(tokens)):
        curr = tokens[i]
        match curr:
            case "AND" | "OR" | "NOT" | "(":
                operators.append(curr)
            case ")":
                while operators[-1] != "(":
                    resolve_two(operands, operators)
                operators.pop()
            case _:
                resolve_one(operands, operators, curr)
        
    while len(operators) > 0:
        resolve_two(operands, operators)

    return operands[0] if len(operands) > 0 else []

def resolve_two(operands: list, operators: list):
    op = operators.pop()
    curr = operands.pop()
    if op == "NOT":
        op = operators.pop()
        operands.append({
            "type": op,
            "value": curr
        })
    else:
        left = operands.pop()                       
        operands.append({
            "type": op,
            "left": left,
            "right": curr
        })

def resolve_one(operands: list, operators: list, curr: str):
    if len(operators) > 0 and operators[-1] == "NOT":
        op = operators.pop()
        operands.append({
            "type": op,
            "value": {"type": "value", "value": curr}
        })
    elif len(operands) > 0:
        left = operands.pop()
        op = operators.pop()                        
        operands.append({
            "type": op,
            "left": left,
            "right": {"type": "value", "value": curr}
        })
    else:
        operands.append(
            {"type": "value", "value": curr}
        )


