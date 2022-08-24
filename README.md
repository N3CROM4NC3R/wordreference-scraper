# wordreference-scraper
Module for scraping words in Wordreference.com, from English to Spanish.

Multiple languages soon.

## Usage

'wordreference-scraper' is used to scrape words and its meanings from the online dictionary "Wordreference"

### One word

```python
from wordreference_scraper.wordreference_scraper import WordreferenceScraper

words = ['get']

wordreference_scraper_instance = WordreferenceScraper(words)

scraped_words = wordreference_scraper_instance.start()

print(scraped_words)
# Dictionary where the keys are the forms of the word
# and the value is the html of all meanings of that word
```

### Multiple words

```python
from wordreference_scraper.wordreference_scraper import WordreferenceScraper

words = ['puzzle', 'noise', 'pencil']

wordreference_scraper_instance = WordreferenceScraper(words)

scraped_words = wordreference_scraper_instance.start()

print(scraped_words)

```
### Selecting sections
Wordreference has multiple sections where shows the multiple meanings of word, such as 'Principal translations', 'Additional translations', 'Verbal Locutions', and 'Compound Forms'. These are the keys and values for the dictionary of sections to scrape

- principal_translations - Boolean: Section for Principal Translations
- additional_translations - Boolean: Section for Additional Translations
- compound_forms - Boolean: Section for Compound Forms
- locuciones_verbales - Boolean: Section for "Locuciones Verbales"

```python
from wordreference_scraper.wordreference_scraper import WordreferenceScraper

words = ['Absolute', 'Note', 'Self']

sections = {
    'principal_translations':True,
    'additional_translations':True,
    'compound_forms':False,
    'locuciones_verbales':False
}

wordreference_scraper_instance = WordreferenceScraper(words,sections)

scraped_words = wordreference_scraper_instance.start()

print(scraped_words)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`wordreference_scraper` was created by Santiago Padron. It is licensed under the terms of the MIT license.

## Credits

`wordreference_scraper` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).






