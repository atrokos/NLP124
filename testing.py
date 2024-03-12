import nltk

def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    lt1, rt1 = t1
    lt2, rt2 = t2

    return (lt1 + lt2, rt1 + rt2)


def check_text(text:list[str], output:list[str]):
    results = (0, 0)
    for text_line, output_line in zip(text, output):
        text_words = nltk.word_tokenize(text_line, language="czech")
        output_words = nltk.word_tokenize(output_line, language="czech")

        if len(text_words) != len(output_words):
            raise RuntimeError(f"Lines do not have the same amount of words!\nText: {text_words}\nOutput: {output_words}")

        for t_word, o_word in zip(text_words, output_words):
            results = add(results, check_word(t_word, o_word))


def check_word(exp: str, act: str) -> tuple[int, int]:
    "Returns the amount of correct out of total."
    if len(exp) != len(act):
        raise RuntimeError(f"Words do not have the same lenght!\n{exp} ; {act}")

    correct: int = sum(map(lambda x: x[0] == x[1], zip(exp, act)))
    total: int = len(exp)
    
    return correct, total

