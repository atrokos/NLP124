from xml.sax.saxutils import escape
import re

def process_allowed(allowed: set[str]) -> set[str]:
    result = set()
    for element in allowed:
        result.update([f"<{element}>", f"</{element}>"])

    return result

def escape_elements(contents: list[str], allowed: set) -> list[str]:
    pattern = re.compile(r".*(</?\S*>).*")

    for i in range(len(contents)):
        line = contents[i]
        if line.startswith("<?") or line.startswith("<!"):
            continue
        if (match := pattern.match(line)):
            if match.group(1) in allowed:
                continue

        contents[i] = escape(line)

    return contents
