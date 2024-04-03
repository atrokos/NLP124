from pathlib import Path

import click
from database import Database
from evaluate import Evaluator


config_cs = {
    "lang": "Czech",
    "tags": {"TITLE", "TEXT", "HEADING"},
    "allowed": {"CZE", "TEXT", "TITLE", "DOCID", "DOCNO", "DATE", "DOC", "GEOGRAPHY", "HEADING"},
    "docs_folder": "./A1/documents_cs",
    "queries_folder": "./A1/topics-train_cs.xml",
    "golds_folder": "./A1/qrels-train_cs.txt",
    "results": "results_cs.txt",
    "statistics": "statistics_cs.txt"
}

config_en = {
    "lang": "English",
    "tags": {"HD", "LD", "TE"},
    "allowed": {'DP', 'WS', 'GO', 'PT', 'LA', 'BR', 'GT', 'DC', 'JP', 'DH', 'SE', 'CR',
                        'CB', 'CP', 'LD', 'PR', 'TI', 'NT', 'WD', 'NO', 'PY', 'HI', 'UP', 'CN', 'DOC',
                        'CF', 'CO', 'SI', 'PG', 'CX', 'FN', 'AU', 'IN', 'DOCID', 'NA', 'TE', 'LATIMES2002',
                        'HD', 'SM', 'BD', 'SP', 'DK', 'EI', 'ID', 'RS', 'IS', 'DF', 'PH', 'DOCNO',
                        'ED', 'DL', 'SL', 'PN', 'PD', 'TM', 'PF', 'KH', 'AN', 'DD', 'CI', 'PP', 'SN'},
    "docs_folder": "./A1/documents_en",
    "queries_folder": "./A1/topics-train_en.xml",
    "golds_folder": "./A1/qrels-train_en.txt",
    "results": "results_en.txt",
    "statistics": "statistics_en.txt"
}

@click.command()
@click.option('-l', '--lang', type=click.Choice(['CS', 'EN', 'both']), help='Choose the language to be evaluated')
@click.option('-i', '--interactive', is_flag=True, default=False, help='Enable interactive mode')
def main(lang, interactive):
    configs = []
    match lang:
        case "CS": configs = [config_cs]
        case "EN": configs = [config_en]
        case "both": configs = [config_cs, config_en]
        case _: return
        
    for config in configs:
        db = Database()
        click.echo(f"Starting database for {config["lang"]}.\n")
        db.load_folder(Path(config["docs_folder"]), config["tags"], config["allowed"])
        db.sort()
        if interactive:
            click.echo("\nStarting an interactive session, you can input queries. Type :quit to quit the session.")
            while (request := input(">>> ")):
                match request:
                    case ":count":
                        click.echo(len(db.entries))
                    case ":quit":
                        return
                    case _:
                        evals = db.evaluate(request)
                        click.echo(evals)
                        click.echo(f"Found {len(evals)} postings.")
            return
                
        all, precision, recall = Evaluator.evaluate_queries(config["queries_folder"], db, config["golds_folder"], config["results"])
        
        with open(config["statistics"], "w") as file:
            file.write("Query ID\tPrecision\tRecall\n")
            for query, prec, rec in all:
                prec_str = "{:.4f}".format(prec)
                rec_str = "{:.4f}".format(rec)
                
                file.write(f"{query}\t{prec_str}\t{rec_str}")
                file.write("\n")
                
            file.write(f"\nAverage precision: {precision}\n")
            file.write(f"Average recall: {recall}\n")

if __name__ == "__main__":
    main()
