from urllib import request
from database import Database
from req_parser import parse_request
from pathlib import Path

if __name__ == "__main__":
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

    while ((prompt := input(">>> ").strip()) != "QUIT"):
        query = parse_request(prompt)
        try:
            print(db.run_query(query))
        except Exception as e:
            print(f"An error has occured:\n{str(e)}")