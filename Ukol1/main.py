from database import Database
from pathlib import Path


if __name__ == "__main__":
    db = Database()
    cs_tags = {"TITLE", "TEXT", "HEADING"}
    en_tags = {"HD", "LD", "TE"}
    en_allowed = {'DP', 'WS', 'GO', 'PT', 'LA', 'BR', 'GT', 'DC', 'JP', 'DH', 'SE', 'CR',
                  'CB', 'CP', 'LD', 'PR', 'TI', 'NT', 'WD', 'NO', 'PY', 'HI', 'UP', 'CN', 'DOC',
                  'CF', 'CO', 'SI', 'PG', 'CX', 'FN', 'AU', 'IN', 'DOCID', 'NA', 'TE', 'LATIMES2002',
                  'HD', 'SM', 'BD', 'SP', 'DK', 'EI', 'ID', 'RS', 'IS', 'DF', 'PH', 'DOCNO',
                  'ED', 'DL', 'SL', 'PN', 'PD', 'TM', 'PF', 'KH', 'AN', 'DD', 'CI', 'PP', 'SN'}
    cs_allowed = {"CZE", "TEXT", "TITLE", "DOCID", "DOCNO", "DATE", "DOC", "GEOGRAPHY", "HEADING"}
    db.load_folder(Path("./Ukol1/A1/documents_cs"), cs_tags, cs_allowed, verbose=True)

    while ((prompt := input(">>> ").strip()) != "QUIT"):
        print(db.evaluate(prompt))

    # found = set()
    # root = ET.parse("./Ukol1/A1/documents_en/la020101.xml").getroot()
    # for doc in root:
    #     for elem in doc:
    #         found.add(elem.tag)

    # print(found)
