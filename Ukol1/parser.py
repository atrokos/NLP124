
"""
"AND" : {
    "value": "Brutus",
    "OR": {
        "value": "Caesar",
        "value": "Pontius"
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
"""
