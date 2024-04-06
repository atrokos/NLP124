from diacritizer import Diacritizer
from testing import check_text
import click

@click.command()
@click.option("-c", "--corpus", type=str, help="Path to the corpus file")
@click.option("-i", "--interactive", is_flag=True, default=False, help='Enable interactive mode')
@click.option("-f", "--file", type=str, help="Path to the input file. Will be ignored if -i is specified.")
@click.option("-v", "--verbose", is_flag=True, default=False, help='Whether to print the diacritized sentence to STDOUT')
def main(corpus, interactive, file, verbose):
    if not corpus:
        print("A path to the corpus must be specified! See --help for more information.")
        return
        
    with open(corpus, "r", encoding="utf-8") as f:
        contents = f.read()
        
    dia = Diacritizer(contents)
    
    if interactive:
        print("Starting interactive session. Write 'QUIT' to end the program.")
        while (sentence := input(">>> ")) != "QUIT":
            result = dia.diacritize(sentence)
            print(result)
            
    else:
        if not file:
            print("A path to an input file must be specified! See --help for more information.")
            return
        
        with open(file, "r", encoding="utf-8") as f:
            text = f.read().splitlines()
            
        text = list(filter(lambda x: len(x.strip()) > 0, text))
        results: list[str] = []
        
        for sentence in text:
            removed_dia = Diacritizer.remove_diacritics(sentence)
            results.append(dia.diacritize(removed_dia))
        
        correct, total = check_text(text, results)
        if verbose: print("\n".join(results))
        print("\n==== Accuracy: ", (correct / total) * 100)



if __name__ == "__main__":
    main()
