# Detect the operating system
ifeq ($(OS),Windows_NT)
	PYTHON_CMD := python
    ACTIVATE_CMD := call .venv/Scripts/activate
else
	PYTHON_CMD := python3
    ACTIVATE_CMD := . .venv/bin/activate
endif

run-data: diacritics-dtest.txt diacritics-etest.txt data/corpus.txt
	( \
       $(ACTIVATE_CMD) && \
       $(PYTHON_CMD) ./src/main.py -c ./data/corpus.txt -f ./diacritics-dtest.txt && \
	   $(PYTHON_CMD) ./src/main.py -c ./data/corpus.txt -f ./diacritics-etest.txt \
    )

all: create-venv packages datasets

create-venv:
	$(PYTHON_CMD) -m venv .venv
	
packages: create-venv requirements.txt
	( \
		$(ACTIVATE_CMD) && \
		pip install -r requirements.txt \
	)
	

datasets: download-data run-data

download-data:
	curl https://ufal.mff.cuni.cz/~zabokrtsky/courses/npfl124/data/diacritics-dtest.txt > ./diacritics-dtest.txt
	curl https://ufal.mff.cuni.cz/~zabokrtsky/courses/npfl124/data/diacritics-etest.txt > ./diacritics-etest.txt

clean:
	(\
		rm ./diacritics-etest.txt && \
		rm -f ./diacritics-dtest.txt && \
		rm -r -f ./.venv && \
		rm -r -f ~/nltk_data \
	)
