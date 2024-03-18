from xml.sax.saxutils import escape
import re

def process_allowed(allowed: set[str]) -> set[str]:
    result = set()
    for element in allowed:
        result.update([f"<{element}>", f"</{element}>"])

    return result

def escape_elements(file: str, allowed: set, /, verbose=False) -> str:
    with open(file, "r", encoding="utf-8") as xml:
        contents = xml.read().splitlines()

    allowed = process_allowed(allowed)
    pattern = re.compile(r".*(</?\S*>).*")

    for i in range(len(contents)):
        line = contents[i]
        if line.startswith("<?") or line.startswith("<!"):
            continue
        if (match := pattern.match(line)):
            if match.group(1) in allowed:
                continue
        
        if verbose:
            print("Escaped: " + line)

        contents[i] = escape(line)

    return "\n".join(contents)


if __name__ == "__main__":
    allowed = {"CZE", "TEXT", "TITLE", "DOCID", "DOCNO", "DATE", "DOC", "GEOGRAPHY", "HEADING"}
    escaped = escape_elements("./Ukol1/ln020225.xml", allowed)

    with open("./Ukol1/result.xml", "w", encoding="utf-8") as xml:
        xml.write(escaped)