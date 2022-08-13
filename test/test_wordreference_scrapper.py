from wordreference_scrapper import WordreferenceScrapper

def test_wordreference_words():
    words = ["get"]
    
    wordreference_scrapper_obj = WordreferenceScrapper(words)

    html_word_list = wordreference_scrapper_obj.start()
 
    test_file = open("./test/text.html","r")
    
    expected_output = test_file.read()
    
    real_output = "".join(html_word_list)

    assert expected_output == real_output