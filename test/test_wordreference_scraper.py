from wordreference_scraper.wordreference_scraper import WordreferenceScraper

def test_getting_one_word():
    words = ["get"]
    
    wordreference_scrapper_obj = WordreferenceScraper(words)

    html_word_list = wordreference_scrapper_obj.start()
 
    test_file = open("./test/one_word.html","r")
    
    expected_output = test_file.read()
    
    real_output = "".join(html_word_list)

    assert expected_output == real_output

def test_getting_multiple_words():
    words = ['about', 'town', 'run']

    wordreference_scrapper_obj = WordreferenceScraper(words)

    html_word_list = wordreference_scrapper_obj.start()
 
    test_file = open("./test/multiple_words.html","r")

    expected_output = test_file.read()
    
    real_output = "".join(html_word_list)

    assert expected_output == real_output
    
def test_getting_sections():

    words = ['Desktop', "Source"]

    sections = {
        'principal_translations':True,
        'additional_translations':True,
        'compound_forms':False,
        'locuciones_verbales':False
    }

    wordreference_scrapper_obj = WordreferenceScraper(words, sections)

    html_word_list = wordreference_scrapper_obj.start()
 
    test_file = open("./test/sections.html","r")

    expected_output = test_file.read()
    
    real_output = "".join(html_word_list)

    assert expected_output == real_output
    
