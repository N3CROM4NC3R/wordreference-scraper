import requests
from bs4 import BeautifulSoup

class WordreferenceScraper ():
    
    """
    Class that contains all process to scrape any word and its meanings
    from english to spanish in the Wordreference's dictonary 
    (wordreference.com)
    
    Attributes
    ----------

    wordreference_url : str
        The url of wordreference that leads to english to spanish translations.
    
    conditionals : dict
        Conditionals that defines what sections to scrape.
        ``"principal_translations"``    
        Contains all information whether this sections('Principal translations') 
        is searchable or not and the title of the html tag that contains all the 
        html tags of the meaning of the word
        (dict)

        ``"additional_translations"``
        Contains all information whether this sections('Additional translations') 
        is searchable or not and the title of the html tag that contains all the 
        html tags of the meaning of the word
        (dict)

        ``"compound_forms"``
        Contains all information whether this sections('Compound forms') 
        is searchable or not and the title of the html tag that contains all the 
        html tags of the meaning of the word
        (dict)

        ``"locuciones_verbales"``
        Contains all information whether this sections('Locuciones verbales') 
        is searchable or not and the title of the html tag that contains all the 
        html tags of the meaning of the word
        (dict)
    """




    # Defining the wordreference url to scrap words, this for spanish translation
    wordreference_url = "https://www.wordreference.com/es/translation.asp?tranword="

    # Defining the sections to translate from the wordreference page
    conditionals = {
        "principal_translations":{"search":True,"section_title":"Principal Translations"},
        "additional_translations":{"search":True,"section_title":"Additional Translations"},
        "compound_forms":{"search":True,"section_title":"Phrasal verbs"},
        "locuciones_verbales":{"search":True,"section_title":"Compound Forms"},
        }


    def __init__(self, word_list, conditionals = dict()):
        """
        Constructor takes a list of words and conditional, this last one
        is a dictionary that defines what are the sections of wordreference
        to scrape.

        Parameters
        ----------  
        word_list : list of str
            List of words to scrape

        conditionals : dict, optional
            Conditionals that defines what sections to scrape.

            ``"principal_translations"``    
            boolean to allow scraping the section "Principal translations"
            (bool)

            ``"additional_translations"``
            boolean to allow scraping the section "Additional translations"
            (bool)

            ``"compound_forms"``
            boolean to allow scraping the section "Compound forms"
            (bool)

            ``"locuciones_verbales"``
            Boolean to allow scraping the section "Locuciones verbales"
            (bool)
        """
        
        self.word_list = word_list

        for key, value in conditionals.items():

            if key in self.conditionals.keys():

                self.conditionals[key]["search"] = value

    
    def start(self):
        """
        To start scraping the words

        Returns
        -------
        dict
            A dictionary that its keys is the words and its values are the meanings and examples
        """

        word_meanings_final = {}

        for word in self.word_list:
            html_text = self.request(word)

            soup = self.create_soup(html_text)

            word_meanings = self.scan_words(soup)
            
            word_meanings_final.update(word_meanings)  
    
        return word_meanings_final

    
    def request(self, word):    
        """
        To make the request to scrape the html of the word
        
        Parameters
        ----------
        word: str
            Word to make the request to scrape the html

        Returns
        -------
        str
            the html of the page of the word
        """

        url = self.wordreference_url + word

        response = requests.get(url)

        return response.text

    
    def create_soup(self, html_text):
        """
        Create a BeautifulSoup object parsing the html.
        
        Parameters
        ----------
        html_text: str
            HTML to parse to a BeautifulSoup object

        Returns
        -------
        BeautifulSoup Object
            The beautiful soup object that contains the html
        """


        soup = BeautifulSoup(html_text, 'html.parser')

        return soup


    def scan_words(self, soup_object):
        """
        Scrape each meaning of the html of the word
        
        Parameters
        ----------
        soup_object: BeautifulSoup object
            THe BeautifulSoup object that contains the html of the word
        
        Returns
        -------
        Dict ['str', 'str']
            The keys are the forms of the word, such as nouns, verbs,
            adjectives, etc, and the values are all html about those
            forms of the word.
        """
        


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
        

    def is_end_question(self,html_tags, html_tag):
        """
        Verifying that the html tag is the last one of the meaning 
        of the form of a word.
        
        Parameters
        ----------
        html_tags: list of str
            Every html tag of the meaning of a form of the word.

        html_tag: str
            Html tag to compare it with the entire list of html tags
            to check whether this is the last one of the meaning 
            of the form of the word
        
        Returns
        -------
        Bool
            Boolean value whether the html tag is the last one or not.
        """

        next_index = html_tags.index(html_tag) + 1
        
        if next_index < len(html_tags):
            next_tag = html_tags[next_index]

            # The last meaning of the form of a word has "id" attribute
            return True if "id" in next_tag.attrs else False

        else:
            return True

    def fill_new_word(self,wrd_tag):
        """
        To make a new meaning of the form of the word

        Parameters
        ----------
        wrd_tag: str of html
            This is the html tag of the form of the word.

        Returns
        -------
        str
            This is the word of a new meaning.
        """

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
