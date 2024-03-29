from typing import Any
from sortedcontainers import SortedList
from database import Database

import xml.etree.ElementTree as ET
from pathlib import Path


class Evaluator:
    def __init__(self):
        self._tags = {"num", "query"}
        pass
         
    def evaluate_queries(self, topics_file: str, db: Database, golds_file: str):
        topics = self._load_topics(topics_file)
        for topic in topics:
            topic["docs"] = set(db.evaluate(topic["query"]))
        
        golds = self._load_gold(golds_file)
        total_tp, total_fp, total_fn = self._get_stats(topics, golds)
        
        return Evaluator.recall(total_tp, total_fn), Evaluator.precision(total_tp, total_fp)
        
    def _load_gold(self, gold_filename: str) -> dict[str, set[str]]:
        golds: dict[str, set[str]] = dict()
        with open(gold_filename, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            
        for line in lines:
            query_id, docid, included = self._parse_gold(line)
            if not included:
                continue
            
            if query_id in golds:
                golds[query_id].add(docid)
            else:
                golds[query_id] = {docid}
                
        return golds
            
            
    def _parse_gold(self, gold: str):
        query_id, _, docid, included = gold.split()
        
        return query_id, docid, bool(int(included))
        
    def _get_stats(self, topics, golds):
        total_tp, total_fp, total_fn = 0, 0, 0
        
        for topic in topics:
            query_id: str = topic["num"]
            found_docs: set[str] = topic["docs"]
            golds_docs = golds[query_id]
            
            tp = len(set.intersection(found_docs, golds_docs))
            fp = len(found_docs) - tp
            fn = len(golds_docs) - tp # TODO Mozna jinak?
            
            total_tp += tp
            total_fp += fp
            total_fn += fn
            
        return total_tp, total_fp, total_fn
    
    @staticmethod
    def recall(tp, fn):
        return tp / (tp + fn)
    
    @staticmethod
    def precision(tp, fp):
        return tp / (tp + fp)
    
    def _load_topics(self, filename: str) -> list[dict[str, Any]]:
        loaded_topics: list[dict[str, Any]] = []
        topics = ET.parse(filename).getroot()
        
        for topic in topics:
            curr = dict()
            for element in topic:
                if element.tag not in self._tags:
                    continue
                
                curr[element.tag] = element.text
            loaded_topics.append(curr)
            
        return loaded_topics
        
    