import nltk

def add(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    lt1, rt1 = t1
    lt2, rt2 = t2

    return (lt1 + lt2, rt1 + rt2)


def check_text(text:list[str], output:list[str]):
    results = (0, 0)
    for text_line, output_line in zip(text, output):
        text_words = nltk.word_tokenize(text_line)
        output_words = nltk.word_tokenize(output_line)


        for t_word, o_word in zip(text_words, output_words):
            results = add(results, check_word(t_word, o_word))
            
    return results


def check_word(exp: str, act: str) -> tuple[int, int]:
    "Returns the amount of correct out of total."
    correct: int = sum(map(lambda x: x[0] == x[1], zip(exp, act)))
    total: int = len(exp)
    
    return correct, total

