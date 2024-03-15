import xml.etree.ElementTree as ET
import re
from pathlib import Path
from sortedcontainers import SortedList, SortedSet

class Database:
    def __init__(self) -> None:
        self.entries = dict[str, SortedList]()
        self._docIDs = SortedList()
        self._last_docID = None
        pass

    def add_entry(self, token: str, docID: str) -> None:
        if self._last_docID != docID:
            self._docIDs.add(docID)
            self._last_docID = docID
            
        if (l := self.entries.get(token, None)) is not None:
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
            
    def _request_value(self, value_name: str) -> SortedList:
        if (l := self.entries.get(value_name, None)) is not None:
            return l
        
        return SortedList()

    def load_file(self, file: Path, tags: set[str]) -> None:
        documents = ET.parse(file).getroot()
        for document in documents:
            if document.tag == "DOC":
                self.add_document(tags, document)
                
    def run_query(self, request: dict) -> SortedList:
        match request["type"]:
            case "AND":
                return self._process_and(request["left"], request["right"])
            case "OR":
                return self._process_or(request["left"], request["right"])
            case "NOT":
                return self._process_not(request["value"])
            case "value":
                return self._request_value(request["value"])
            case _:
                raise RuntimeError("Unknown request type: " + request["type"])
            
    def _process_and(self, left: dict, right: dict) -> SortedList:
        left = self.run_query(left)
        right = self.run_query(right)
        result = SortedList()
        l, r = 0, 0
        while l < len(left) and r < len(right):
            if left[l] == right[r]:
                result.add(left[l])
                l += 1
                r += 1
            elif left[l] < right[r]:
                l += 1
            else:
                r += 1
        
        return result
        
    def _process_or(self, left: dict, right: dict) -> SortedList:
        left = self.run_query(left)
        right = self.run_query(right)
        result = SortedList()
        l, r = 0, 0
        while l < len(left) and r < len(right):
            if left[l] == right[r]:
                result.add(left[l])
                l += 1
                r += 1
            elif left[l] < right[r]:
                result.add(left[l])
                l += 1
            else:
                result.add(right[r])
                r += 1
                
        if l < len(left):
            result.update(left[l:])
            
        if r < len(right):
            result.update(right[r:])
        
        return result
    
    def _process_not(self, value: dict) -> SortedList:
        value = self.run_query(value)
        result = SortedList()
        v, i = 0, 0
        while v < len(value) and i < len(self._docIDs):
            if self._docIDs[i] != value[v]:
                result.add(self._docIDs[i])
                i += 1
            else:
                v += 1
                i += 1
                
        if v < len(value) and i < len(self._docIDs) and self._docIDs[i] > value[v]:
            result.update(self._docIDs[i:])
        
        return result
        

def tokenize(sentence: str | None) -> list[str]:
    if sentence is None:
        raise RuntimeError("Expected a sentence, got None.")
    
    tokens = re.findall(r'\b\w+\b', sentence)

    return tokens