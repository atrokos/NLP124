## Instrukce ke spuštění
Pro bezproblémový běh je potřeba Python ve verzi 3.12.
Doporučuji si udělat virtuální prostředí:\
`python -m venv venv`

A pak ho aktivovat:\
`./venv/Scripts/activate`, popř. `source ./venv/bin/activate`

Nakonec stačí nainstalovat potřebné balíčky pomocí:\
`pip install -r requirements.txt`

Nyní se dá program spustit jednoduše pomocí `python ./src/main.py --lang both`

`--lang both` říká programu, ať zpracuje anglické a české dokumenty + jejich dotazy. Pokud chcete vyzkoušet libovolný dotaz interaktivně, stačí přidat argument `--interactive`.

**Vstupní soubory musí být ve složce A1, která musí být v kořeni projektu.** Program předpokládá stejnou strukturu složky A1, jako byla při zadání. V případě potřeby si lze upravit tyto cesty v `main.py`, konkrétně `config_cs` a `config_en`.


## Program
### Stav XML souborů
U obou jazyků jsem narazil na problém s validitou vstupních XML souborů - někde byly špatně uzavřené elementy, jinde byly neplatné znaky.

To jsem vyřešil třídou `Preprocessor`, která opraví případné poškozené XML soubory na validní tak, aby byl jejich obsah co nejvíce zachován. Z povahy chyb ve vstupních dokumentech jsem musel bohužel sáhnout k poměrně specifickým opravám, takže na jiné soubory to nemusí dokonale fungovat.

### Indexace
O indexaci souborů se stará třída `Database`, která načte již opravené XML soubory a jednoduše je zindexuje pomocí `dict` a `sortedlist`.

### Dotazy
Dotazy pomáhá databázi zpracovat `QueryParser`, který vrátí `dict` obsahující abstraktní strom dotazu. Samotná databáze pak převezme tento strom a podle něj zpracuje příslušné příkazy.

### Zpracování trénovacích dat
Trénovací dotazy a jejich výsledky načte `Evaluator`, který se pak dotazuje na databázi a následně porovnává obdržené dokumenty. Nakonec spočítá přesnost a recall: průměrný i pro jednotlivé dotazy.

## Výsledky dotazů
Překvapily mě nízké hodnoty recallu i přesnosti u obou jazyků (i když čeština je mnohem horší). Když jsem to více zkoumal, tak jsem zjistil, že se do indexace pravděpodobně měla brát i data článků (jinak např. dotaz s číslem 2002 nesprávně ignoroval články z roku 2002).

Pak jsem narazil na případy, kdy by normalizace slov i dotazů výrazně pomohla (třeba program "nesprávně" ignoroval články, které sice obsahovaly chtěná slova, ale v jiném pádu či čísle).

Zajímavé bylo, že jsem naopak narazil na výsledky dotazů, které byly správné (opravdu obsahovala dotazovaná slova), ale podle trénovacích dat tam být němely.
