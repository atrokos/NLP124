from calendar import c
import nltk
import re
from collections import Counter

LETTERS_NODIA = "acdeeinorstuuyz"
LETTERS_DIA = "áčďéěíňóřšťúůýž"
DIA_TO_NODIA = str.maketrans(LETTERS_DIA, LETTERS_NODIA)
bigram_t = tuple[str, str]

def clean_up_text(text: str) -> tuple[list[str], list[str]]:
    result: list[str] = []
    text_split: list[str] = text.splitlines()
    for sentence in text_split:
        sentence = sentence.lower().split()
        result.append(" ".join(sentence))

    result: list[str] = list(filter(lambda x : len(x) > 0, result))
    nodia = list(map(lambda x: x.translate(DIA_TO_NODIA), result))
    return result, nodia

def get_bigrams(text: list[str]) -> Counter[tuple[str,str]]:
    bigrams = Counter[tuple[str,str]]()

    for line in text:
        bigrams.update(nltk.bigrams(nltk.word_tokenize(line, language="czech")))
        

    return bigrams

def get_trigrams(text: list[str]) -> Counter[tuple[str,str,str]]:
    trigrams = Counter[tuple[str,str,str]]()

    for line in text:
        words: list[str] = nltk.word_tokenize(line, language="czech")
        for word in words:
            w_space: str = "\0" + word + "\0"
            trigrams.update(nltk.trigrams(w_space))

    return trigrams

def word_bigrams(dia: list[str]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = dict()
    bigrams = get_bigrams(dia)

    for cword, wword in bigrams:
        cword_nodia = cword.translate(DIA_TO_NODIA)
        wword_nodia = wword.translate(DIA_TO_NODIA)
        if cword in result:
            d = result[cword_nodia]

            if wword_nodia in d:
                if bigrams[(cword, wword)] > bigrams[(cword, d[wword_nodia])]:
                    result[cword_nodia][wword_nodia] = wword
            else:
                result[cword_nodia][wword_nodia] = wword
        else:
            result[cword_nodia] = {wword_nodia : wword}

    return result

def letter_trigrams(dia: list[str]) -> dict[bigram_t, dict[str, str]]:
    result: dict[bigram_t, dict[str, str]] = dict()
    trigrams = get_trigrams(dia)

    for c1, c2, w in trigrams:
        trigram = (c1, c2, w)
        bigram = (c1.translate(DIA_TO_NODIA), c2.translate(DIA_TO_NODIA))
        w_nodia: str = w.translate(DIA_TO_NODIA)
        if bigram in result:
            d = result[bigram]
            if w_nodia in d:
                if trigrams[trigram] > trigrams[(c1, c2, d[w_nodia])]: # if there are more usages of the new trigram than the old one, change it to the new trigram
                    result[bigram][w_nodia] = w
            else:
                result[bigram][w_nodia] = w
        else:
            result[bigram] = {w_nodia : w}

    return result

def letter_trigrams_2(dia: list[str]) -> dict[bigram_t, dict[str, str]]:
    result: dict[bigram_t, dict[str, str]] = dict()
    trigrams = get_trigrams(dia)

    for c1, w, c2 in trigrams:
        trigram = (c1, w, c2)
        bigram = (c1.translate(DIA_TO_NODIA), c2.translate(DIA_TO_NODIA))
        w_nodia: str = w.translate(DIA_TO_NODIA)
        if bigram in result:
            d = result[bigram]
            if w_nodia in d:
                if trigrams[trigram] > trigrams[(c1, d[w_nodia], c2)]: # if there are more usages of the new trigram than the old one, change it to the new trigram
                    result[bigram][w_nodia] = w
            else:
                result[bigram][w_nodia] = w
        else:
            result[bigram] = {w_nodia : w}

    return result

def naive_sol(dia: list[str], nodia: list[str]):
    mapping = dict()

    for i in range(len(dia)):
        dia_line = dia[i].split()
        nodia_line = nodia[i].split()
        mapping.update(zip(nodia_line, dia_line))
    
    mapping["ze"] = "ze"
    return mapping

def run_trigram_model(word: str, trimodel: dict[bigram_t, dict[str, str]]) -> str:
    space_word = "\0" + word + "\0"
    result: list[str] = []
    for c1, w, c2 in nltk.trigrams(space_word):
        if (c1, c2) in trimodel:
            result.append(trimodel[(c1, c2)].get(w, w))
        else:
            result.append(w)

    return "".join(result)


if __name__ == "__main__":
    with open("corpus.txt", "r", encoding="utf-8") as f:
        contents = f.read()

    print(len("Atimsedostavamekestezejnimotazkamtohototextu:Jakyvlastnejemocenskyvztahprirodyakultury?Nakolikjevulepodporovanaznalostmiainteligencischopnablokovattynegativnizodvekychlidskychpudu,instinktu,emoci–takovych,dikynimzjsmesekdysizadobledovych,hladomoruivselikychpohromprocpaliuzkymhrdlemvyvoje,alekterednespronasjakocelekpredstavujinastrojemoralnihohazardu?Dojakemirydokazemeposlouchatsvujrozum?Muzekulturnievolucepreprattoprezilezdedictvievolucebiologicke?Svedoumemypozmenitgeny?Nakolikdokazemeposunoutsklenenystropprirozenosti,oddelujicidohlednutelneoddosazitelneho?"))
    # dia, nodia = clean_up_text(contents)
    # dic = naive_sol(dia, nodia)
    # trigrams = letter_trigrams_2(dia)
    # bigrams = word_bigrams(dia)
    # line: str = input(">>> ")

    # result = []
    # for prev, word in nltk.bigrams(nltk.word_tokenize("\0 " + line.lower(), language="czech")):
    #     try:
    #         result.append(bigrams[prev][word])
    #     except KeyError:
    #         try:
    #             result.append(dic[word])
    #         except KeyError:
    #             result.append(run_trigram_model(word, trigrams))

    # print(" ".join(result))
