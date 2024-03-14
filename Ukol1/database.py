import xml.etree.ElementTree as ET
import re
from pathlib import Path
from bisect import insort
from sortedcontainers import SortedList
from regex import D

class Database:
    def __init__(self) -> None:
        self.entries = dict[str, SortedList]()
        pass

    def add_entry(self, token: str, docID: str) -> None:
        if (l := self.entries.get(token, None)) is not None:
            if docID not in l:
                l.add(docID)
        else:
            self.entries[token] = SortedList([docID])

    def add_document(self, tags: set[str], document: ET.Element) -> None:
        """
        Add the given document to the database db, extracting only the given tags.
        """
        found_element = document.find("DOCID")
        if found_element is None:
            raise RuntimeError("The given document does not have DOCID!")
        
        docID = found_element.text
        tokens: set[str] = set()

        for child in document:
            if child.tag not in tags:
                continue

            tokens.update(tokenize(child.text))

        for token in tokens:
            self.add_entry(token, docID) # type: ignore

    def load_file(self, file: Path, tags: set[str]) -> None:
        documents = ET.parse(file).getroot()
        for document in documents:
            if document.tag == "DOC":
                self.add_document(tags, document)

def tokenize(sentence: str | None) -> list[str]:
    if sentence is None:
        raise RuntimeError("Expected a sentence, got None.")
    
    tokens = re.findall(r'\b\w+\b', sentence)

    return tokens

db = Database()
cs_tags = {"TITLE", "TEXT", "HEADING"}

for file in Path("./Ukol1/A1/documents_cs").iterdir():
    if not file.name.endswith(".xml"):
        continue
    try:
        print(f"Processing {file}")
        db.load_file(file, cs_tags)
    except Exception as e:
        print(f"Could not load: {file}")

while ((prompt := input()) != ""):
    try:
        print(db.entries[prompt])
    except:
        print("Key not found!")