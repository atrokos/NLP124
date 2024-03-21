import re

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
"""

class QueryParser:
    def __init__(self) -> None:
        self._operands = []
        self._operators = []

    @staticmethod
    def _tokenize_command(comm: str) -> list[str]:
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
    def _parse_command(self, tokens: list[str]):
        for i in range(len(tokens)):
            curr = tokens[i]
            match curr:
                case "AND" | "OR" | "NOT" | "(":
                    self._operators.append(curr)
                case ")":
                    while self._operators[-1] != "(":
                        self._resolve_two()
                    self._operators.pop()
                case _:
                    self._resolve_one(curr)
            
        while len(self._operators) > 0:
            self._resolve_two()

        return self._operands[0] if len(self._operands) > 0 else {"type" : "null"}

    def _resolve_two(self):
        op = self._operators.pop()
        curr = self._operands.pop()
        if op == "NOT":
            op = self._operators.pop()
            self._operands.append({
                "type": op,
                "value": curr
            })
        else:
            left = self._operands.pop()                       
            self._operands.append({
                "type": op,
                "left": left,
                "right": curr
            })

    def _resolve_one(self, curr: str):
        if len(self._operators) > 0 and self._operators[-1] == "NOT":
            op = self._operators.pop()
            self._operands.append({
                "type": op,
                "value": {"type": "value", "value": curr}
            })
        elif len(self._operands) > 0 and self._operators[-1] != "(":
            left = self._operands.pop()
            op = self._operators.pop()                        
            self._operands.append({
                "type": op,
                "left": left,
                "right": {"type": "value", "value": curr}
            })
        else:
            self._operands.append(
                {"type": "value", "value": curr}
            )

    def parse_request(self, request: str) -> dict:
        self._operands = []
        self._operators = []
        return self._parse_command(QueryParser._tokenize_command(request))

    @staticmethod
    def tokenize(sentence: str | None) -> list[str]:
        if sentence is None:
            return [""]
        
        tokens = re.findall(r'\b\w+\b', sentence)

        return tokens