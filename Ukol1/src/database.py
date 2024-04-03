import xml.etree.ElementTree as ET
import tempfile
from pathlib import Path

from click import progressbar

from preprocessor import Preprocessor
from queryparser import QueryParser

class Database:
    def __init__(self) -> None:
        self.entries = dict()
        self._docIDs = set()
        self._last_docID = None
        self._temp_file = tempfile.TemporaryDirectory()
        self._parser = QueryParser()
        pass
    
    def __del__(self):
        self._temp_file.cleanup()
        
    @staticmethod
    def count_xml_files(path: Path):
        # Returns the amount of XML files in the directory (not recursive).
        count = 0
        for item in path.iterdir():
            if item.is_file():
                count += 1
                
        return count

    def load_folder(self, folder: Path, tags: set[str], allowed: set[str]) -> None:
        """
        Indexes all XML files present in the directory (not recursive).
        """
        if not folder.exists():
            raise FileNotFoundError("This app assumes that the A1 input file is in the root directory of the project.")
        
        path = Path(self._temp_file.name)
        count = self.count_xml_files(folder)
        preprocessor = Preprocessor(allowed)
        preprocessor.preprocess_inputs(folder, path, count)
        
        with progressbar(path.iterdir(), label="Indexing documents ", length=count) as files:
            for file in files:
                if not file.name.endswith(".xml"):
                    continue

                documents = ET.parse(file).getroot()
                for document in documents:
                    if document.tag == "DOC":
                        self._add_document(tags, document)

    def sort(self):
        self._docIDs = sorted(self._docIDs)
        for key in self.entries.keys():
            self.entries[key] = sorted(self.entries[key])


    def evaluate(self, request: str) -> list:
        # Evaluates the query and returns all relevant documents in a list.
        try:
            query = self._parser.parse_request(request)
            return self._run_query(query)
        except Exception as e:
            print(f"An error has occured when processing request \"{request}\":\n" + str(e))
            return []

    def _add_entry(self, token: str, docID: str) -> None:
        self._docIDs.add(docID)
            
        if (l := self.entries.get(token, None)) is not None:
            l.add(docID)
        else:
            self.entries[token] = {docID}

    def _add_document(self, tags: set[str], document: ET.Element) -> None:
        """
        Add the given document to the database db, extracting only the given tags.
        """
        found_element = document.find("DOCID")
        if found_element is None:
            raise RuntimeError("The given document does not have DOCID!")
        
        docID = found_element.text

        for child in document:
            if child.tag not in tags:
                continue
            
            for token in QueryParser.tokenize(child.text):
                self._add_entry(token, docID)
            
    def _request_value(self, value_name: str) -> list[str]:
        if (l := self.entries.get(value_name, None)) is not None:
            return l
        
        return []
                
    def _run_query(self, request: dict) -> list[str]:
        match request["type"]:
            case "AND":
                return self._process_and(request["left"], request["right"])
            case "OR":
                return self._process_or(request["left"], request["right"])
            case "NOT":
                return self._process_not(request["value"])
            case "value":
                return self._request_value(request["value"])
            case "null":
                return []
            case _:
                raise RuntimeError("Unknown request type: " + request["type"])
            
    def _process_and(self, left: dict, right: dict) -> list[str]:
        left = self._run_query(left)
        right = self._run_query(right)
        result = []
        l, r = 0, 0
        while l < len(left) and r < len(right):
            if left[l] == right[r]:
                result.append(left[l])
                l += 1
                r += 1
            elif left[l] < right[r]:
                l += 1
            else:
                r += 1
        
        return result
        
    def _process_or(self, left: dict, right: dict) -> list[str]:
        left = self._run_query(left)
        right = self._run_query(right)
        result = []
        l, r = 0, 0
        while l < len(left) and r < len(right):
            if left[l] == right[r]:
                result.append(left[l])
                l += 1
                r += 1
            elif left[l] < right[r]:
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
                
        if l < len(left):
            result.extend(left[l:])
            
        if r < len(right):
            result.extend(right[r:])
        
        return result
    
    def _process_not(self, value: dict) -> list[str]:
        postings = self._run_query(value)
        result = []
        i = 0
        for doc in self._docIDs:
            if i < len(postings) and doc == postings[i]:
                i += 1
                continue
            result.append(doc)
        
        return result
