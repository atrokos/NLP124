from typing import Optional
"""
{
    "type": AND,
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
        },
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

Handling NOT => diff with w
=> must have an implicit ALL AND (User command)

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

def parse_command(tokens: list[str]) -> dict:
    saved_comm = None
    result = dict()
    


print(tokenize_command("Caesar AND Brutus OR (WHatever OR HE)"))
