import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from collections import Counter

bigram_t = tuple[str, str]
class Diacritizer:
    LETTERS_NODIA = "acdeeinorstuuyz"
    LETTERS_DIA = "áčďéěíňóřšťúůýž"
    DIA_TO_NODIA = str.maketrans(LETTERS_DIA, LETTERS_NODIA)
    
    def __init__(self, contents):
        dia, nodia = self._clean_up_text(contents)
        print("Training word bigrams...")
        self.bigrams = self._word_bigrams(dia)
        print("Training word unigrams...")
        self.dic = self._naive_sol(dia, nodia)
        print("Training letter trigrams...")
        self.trigrams = self._letter_trigrams(dia)

    def _clean_up_text(self, text: str) -> tuple[list[str], list[str]]:
        result: list[str] = []
        text_split: list[str] = text.splitlines()
        for sentence in text_split:
            sentence = sentence.lower().split()
            result.append(" ".join(sentence))

        result: list[str] = list(filter(lambda x : len(x) > 0, result))
        nodia = list(map(lambda x: x.translate(self.DIA_TO_NODIA), result))
        return result, nodia

    def _get_bigrams(self, text: list[str]) -> Counter[tuple[str,str]]:
        bigrams = Counter[tuple[str,str]]()

        for line in text:
            bigrams.update(nltk.bigrams(nltk.word_tokenize(line)))
            
        return bigrams

    def _get_trigrams(self, text: list[str]) -> Counter[tuple[str,str,str]]:
        trigrams = Counter[tuple[str,str,str]]()

        for line in text:
            words: list[str] = nltk.word_tokenize(line)
            for word in words:
                w_space: str = "\0" + word + "\0"
                trigrams.update(nltk.trigrams(w_space))

        return trigrams

    def _word_bigrams(self, dia: list[str]) -> dict[str, dict[str, str]]:
        result: dict[str, dict[str, str]] = dict()
        bigrams = self._get_bigrams(dia)

        for cword, wword in bigrams:
            cword_nodia = cword.translate(self.DIA_TO_NODIA)
            wword_nodia = wword.translate(self.DIA_TO_NODIA)
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

    def _letter_trigrams(self, dia: list[str]) -> dict[bigram_t, dict[str, str]]:
        result: dict[bigram_t, dict[str, str]] = dict()
        trigrams = self._get_trigrams(dia)

        for c1, w, c2 in trigrams:
            trigram = (c1, w, c2)
            bigram = (c1.translate(self.DIA_TO_NODIA), c2.translate(self.DIA_TO_NODIA))
            w_nodia: str = w.translate(self.DIA_TO_NODIA)
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

    def _naive_sol(self, dia: list[str], nodia: list[str]):
        mapping = dict()

        for i in range(len(dia)):
            dia_line = dia[i].split()
            nodia_line = nodia[i].split()
            mapping.update(zip(nodia_line, dia_line))
        
        mapping["ze"] = "ze"
        return mapping

    def _run_trigram_model(self, word: str) -> str:
        space_word = "\0" + word + "\0"
        result: list[str] = []
        for c1, w, c2 in nltk.trigrams(space_word):
            if (c1, c2) in self.trigrams:
                result.append(self.trigrams[(c1, c2)].get(w, w))
            else:
                result.append(w)

        return "".join(result)
    
    def _restore_capitals(self, orig: str, new: str) -> str:
        result = []
        for o, n in zip(orig, new):
            if o.isupper():
                result.append(n.upper())
            else:
                result.append(n)
                
        return "".join(result)

    def diacritize(self, sentence: str) -> str:
        result = []
        for prev, word in nltk.bigrams(nltk.word_tokenize("\0 " + sentence)):
            prev = prev.lower()
            word = word.lower()
            try:
                result.append(self.bigrams[prev][word])
            except KeyError:
                try:
                    result.append(self.dic[word])
                except KeyError:
                    result.append(self._run_trigram_model(word))

        detokenized = TreebankWordDetokenizer().detokenize(result)
        norm_sentence = TreebankWordDetokenizer().detokenize(nltk.word_tokenize(sentence))
        return self._restore_capitals(norm_sentence, detokenized)
    
    @staticmethod
    def remove_diacritics(text: str) -> str:
        LETTERS_NODIA = "acdeeinorstuuyz"
        LETTERS_DIA = "áčďéěíňóřšťúůýž"
        DIA_TO_NODIA = text.maketrans(LETTERS_DIA, LETTERS_NODIA)
        return text.translate(DIA_TO_NODIA)
        