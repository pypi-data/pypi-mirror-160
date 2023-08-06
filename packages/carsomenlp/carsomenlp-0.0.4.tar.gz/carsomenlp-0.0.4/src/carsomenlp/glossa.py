from carsomenlp import translator
from carsomenlp import wrangler
from carsomenlp import tokenizer
from carsomenlp import matcher
import logging

logging.getLogger().setLevel(logging.INFO)

class Glossa:
    def __init__(self) -> None:
        pass

    def translate(self, text):
        """Translater text to english
        Args:
            text (str): query from user
        Returns:
            (str): Translated text in english
        """
        try:
            translated_text = translator.to_english(text)
        except Exception as e:
            logging.error(f"Cannot translate due to : {e} ")
            
        return translated_text
    
    def clean(self, text):
        """Clean query string relative to car information

        Args:
            text (str): query string

        Returns:
            str: cleaned text
        """
        brand_fixed = wrangler.fix_brand(text)
        space_fixed = wrangler.fix_space(brand_fixed)
        
        return space_fixed

    def tokenize(self,text):
        """Seperate chunks of words from text

        Args:
            text (_type_): string query

        Returns:
            list: chunk of words
        """
        try: 
            tokens = tokenizer.tokenize(text)
            return tokens
        except Exception as e:
            logging.error(f"Failed to tokenize in glossa due to:{e}")
            
    def match(self, tokens):
        """ Match tokens of words with car information

        Args:
            tokens (list): Chunks of keywords from text

        Returns:
            dict: Information of matched tokens
        """
        try:
            
            if type(tokens) == str:
                tokens = self.tokenize(tokens)
                
            matches = matcher.exact_match(tokens)
            
            if matches['model'] is None or matches['brand'] is None:
                matches = matcher.fuzzy_match_brand_model(matches, tokens)
            
            return matches
            
        except Exception as e:
            logging.error(f"Failed to match in glossa due to:{e}")

    def extract(self, text):
        """ Extract car information on given text. This run the text through the whole Glossa NLP

        Args:
            text (str): String quer

        Returns:
            dict: Extracted information
        """
        cleaned_text = self.clean(text)
        translated = self.translate(cleaned_text)
        tokenized = self.tokenize(translated)
        matched = self.match(tokenized)
        
        return matched