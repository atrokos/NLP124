import xml.etree.ElementTree as ET
from typing import Any

from click import progressbar

from database import Database


class Evaluator:
    _tags = {"num", "query"}
         
    @staticmethod
    def evaluate_queries(topics_file: str, db: Database, golds_file: str, results_file: str):
        topics = Evaluator._load_topics(topics_file)
        for topic in topics:
            results = db.evaluate(topic["query"])
            with open(results_file, "a") as file:
                for result in results:
                    file.write(topic["num"] + " " + result + "\n")

            topic["docs"] = set(results)
        
        golds = Evaluator._load_gold(golds_file)
        return Evaluator._get_stats(topics, golds)
        
    @staticmethod
    def _load_gold(gold_filename: str) -> dict[str, set[str]]:
        golds: dict[str, set[str]] = dict()
        with open(gold_filename, "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
            
        for line in lines:
            query_id, docid, included = Evaluator._parse_gold(line)
            if not included:
                continue
            
            if query_id in golds:
                golds[query_id].add(docid)
            else:
                golds[query_id] = {docid}
                
        return golds
            
    @staticmethod
    def _parse_gold(gold: str):
        query_id, _, docid, included = gold.split()
        
        return query_id, docid, bool(int(included))
        
    @staticmethod
    def _get_stats(topics, golds):
        all_stats = []
        total_prec, total_rec = 0, 0
        
        with progressbar(topics, label="Evaluating queries ") as p_topics:
            for topic in p_topics:
                query_id: str = topic["num"]
                found_docs: set[str] = topic["docs"]
                golds_docs = golds[query_id]
                
                tp = len(set.intersection(found_docs, golds_docs))
                fp = len(found_docs) - tp
                fn = len(golds_docs) - tp # TODO Mozna jinak?
                
                precision = Evaluator.precision(tp, fp)
                recall = Evaluator.recall(tp, fn)
                total_prec += precision
                total_rec += recall
                
                all_stats.append((query_id, precision, recall))
            
        return all_stats, total_prec / len(topics), total_rec / len(topics)
    
    @staticmethod
    def recall(tp, fn):
        if tp + fn == 0:
            return 0.
        return tp / (tp + fn)
    
    @staticmethod
    def precision(tp, fp):
        if tp + fp == 0:
            return 0.
        return tp / (tp + fp)
    
    @staticmethod
    def _load_topics(filename: str) -> list[dict[str, Any]]:
        loaded_topics: list[dict[str, Any]] = []
        topics = ET.parse(filename).getroot()
        
        for topic in topics:
            curr = dict()
            for element in topic:
                if element.tag not in Evaluator._tags:
                    continue
                
                curr[element.tag] = element.text
            loaded_topics.append(curr)
            
        return loaded_topics
        
    