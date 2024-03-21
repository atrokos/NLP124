from typing import Optional

"""
{
    "type": "AND",
    "left": {
        "type": "value",
        "value": "Brutus"
    },
    "right": {
        "type": "OR",
        "left": {
            "type": "value",
            "value": "Caesar"
        },
        "right": {
            "type": "value",
            "value": "Pontius"
        }
    }
}

- is equivalent to: Brutus AND (Caesar OR Pontius)

Process:
1) AND, value => get all documents with Brutus
2) AND, OR => recursive call on OR
    1) OR, value => get all documents with Caesar
    2) OR, value => get all documents with Pontius
    3) All values processed => unionize [Caesar] with [Pontius]
    4) return result
3) All values processed => intersect [Brutus] with [Caesar U Pontius]

First always evaluate user command. If it is not a NOT, throw ALL away.
"""

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


