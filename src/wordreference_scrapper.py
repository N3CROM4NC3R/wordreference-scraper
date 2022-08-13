import requests
from bs4 import BeautifulSoup

class WordreferenceScrapper ():
    
    # Defining the wordreference url to scrap words, this for spanish translation
    wordreference_url = "https://www.wordreference.com/es/translation.asp?tranword="

    # Defining the sections to translate from the wordreference page
    conditionals = {
        "PT":{"search":True,"section_title":"Principal Translations"},
        "AT":{"search":True,"section_title":"Additional Translations"},
        "CF":{"search":True,"section_title":"Phrasal verbs"},
        "LV":{"search":True,"section_title":"Compound Forms"},
        }

    # Constructor take the arguments List of words, conditionals(Sections to translate)
    # and the deck name
    def __init__(self, list_words, conditionals = dict()):
        
        self.list_words = list_words

        for key, value in conditionals.items():
            self.conditionals[key]["search"] = value

    # Start the scrapping and returning the words
    def start(self):
        
        word_meanings_final = {}

        for word in self.list_words:
            html_text = self.request(word)

            soup = self.create_soup(html_text)

            word_meanings = self.scan_words(soup)
            
            word_meanings_final.update(word_meanings)  
    
        return word_meanings_final

    # Making the request
    # Building the complete url and returning the html of word
    def request(self, word):    
        
        url = self.wordreference_url + word

        response = requests.get(url)

        return response.text

    # Returning a BeautifulSoup object through the html text of the word
    def create_soup(self, html_text):
        
        soup = BeautifulSoup(html_text, 'html.parser')

        return soup

    # Extracting the html of each meaning of the word that are into the
    # sections allowed
    def scan_words(self, soup_object):
        # The tag that has all words, its forms and its meanings
        wrd_tags = soup_object.select('.WRD')

        # The allowed wrd tags to scrap
        allowed_wrd_tags = []
 
        # Taking the piece of html that are into the allowed sections
        for wrd_tag in wrd_tags:
            
            for condition_info in self.conditionals.values():
                
                section_title = wrd_tag.select('.wrtopsection td')[0].attrs["title"]

                if(condition_info["search"] == True and section_title == condition_info["section_title"]):
                    
                    allowed_wrd_tags += wrd_tag.select('.even, .odd')
                    
                    break
        
        words_and_meanings = {}

        word = ""
        meaning = ""

        completed_words = []
        
        # Html tags of the words
        for wrd_tag in allowed_wrd_tags:
            
            # If it is a new word to scrap
            if word == "":
                word = self.fill_new_word(wrd_tag)

            # The meanings and examples of each section
            meaning += str(wrd_tag)
            
            # If it is the end of the html in a meaning
            if self.is_end_question(allowed_wrd_tags, wrd_tag):
                # if the meaning is a new one    
                if not (word in completed_words):
                    words_and_meanings[word] = meaning
                else:
                    words_and_meanings[word] += meaning
                
                ## Recording the scrapped meanings and words
                completed_words.append(word)
                

                # Emptying the word and meaning to scrap a new one
                word = ""
                meaning = ""
            
        return words_and_meanings
        
    # Method to make sure that a tag of the meaning is the last one
    # of the group of tags that the meaning has
    def is_end_question(self,html_tags, html_tag):
        next_index = html_tags.index(html_tag) + 1
        
        if next_index < len(html_tags):
            next_tag = html_tags[next_index]

            # The last meaning of the form of a word has "id" attribute
            return True if "id" in next_tag.attrs else False

        else:
            return True

    # Creating a new word
    def fill_new_word(self,wrd_tag):
        # Variable for the title of the question
        word_title = ""
        
        # The tag where the word is
        word_tag = wrd_tag.select(".FrWrd")[0]

        # The word
        note_word_question_tag = word_tag.select("strong")[0]
        
        # This is to check whether the verb is transitive and it has
        # a object, this is the allowed titles of the span tag
        # Where the name of the object is.
        allowed_titles = ["something", "somebody","something or somebody","somebody or something"]
        
        # Creating the word title, with the word/verb and its object
        for note_word_question in note_word_question_tag.contents:
    
            if isinstance(note_word_question, str) or len(note_word_question.attrs) != 0 and note_word_question.attrs["title"] in allowed_titles:
                word_title += str(note_word_question) 

        # Checking what is the type of word
        # Eg: Adjective, verb, transitive verb, intransitive verb, noun, etc.
        word_type_tag = word_tag.select(".POS2")[0]
        word_type = word_type_tag.contents

        if len(word_type) > 0:
            word_type_text = word_type[0]
            word_title += " <strong>" + str(word_type_text) + "</strong>"
        
        return word_title
