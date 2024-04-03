from xml.sax.saxutils import escape
import re


def process_skipped(skipped: set[str]) -> set[str]:
    """
    Simply adds all XML elements (opening and closing) to a set.
    """
    result = set()
    for element in skipped:
        result.update([f"<{element}>", f"</{element}>"])

    return result

def escape_elements(contents: list[str], skipped: set) -> list[str]:
    """
    Escapes all invalid XML character present in contents. If the string contains
    an element in allowed, it is skipped.
    """
    pattern = re.compile(r".*(</?\S*>).*")

    for i in range(len(contents)):
        line = contents[i]
        if line.startswith("<?") or line.startswith("<!"):
            continue
        if (match := pattern.match(line)):
            if match.group(1) in skipped:
                continue

        contents[i] = escape(line)

    return contents
