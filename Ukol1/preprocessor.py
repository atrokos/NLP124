from xml.sax.saxutils import escape
import re
from pathlib import Path

class Preprocessor:
    def __init__(self, allowed: set[str]):
        self._allowed = Preprocessor._process_allowed(allowed)

    def preprocess_inputs(self, folder: Path, out: Path, /, verbose=False):
        for file in folder.iterdir():
            if not file.name.endswith(".xml"):
                continue
            
            if verbose: print("Preprocessing " + str(file) + "... ", end="")
            with open(file, "r", encoding="utf-8") as xml:
                contents = xml.read().splitlines()

            contents_fixed = Preprocessor._escape_elements(contents, self._allowed)
            
            target = out.joinpath(file.name)
            with open(target, "w", encoding="utf-8") as xml:
                xml.write("\n".join(contents_fixed))

            if verbose: print("done")

    
    @staticmethod
    def _process_allowed(allowed: set[str]) -> set[str]:
        result = set()
        for element in allowed:
            result.update([f"<{element}>", f"</{element}>"])

        return result

    @staticmethod
    def _escape_elements(contents: list[str], allowed: set) -> list[str]:
        pattern = re.compile(r".*(</?\S*>).*")

        for i in range(len(contents)):
            line = contents[i]
            line = line.replace("", "")
            if line.startswith("<?") or line.startswith("<!"):
                continue
            if (match := pattern.match(line)):
                if "</LATIMES2002></LATIMES2002>" in line:
                    line = "</LATIMES2002>"
                contents[i] = line
                if match.group(1) in allowed:
                    continue

            contents[i] = escape(line)

        return contents