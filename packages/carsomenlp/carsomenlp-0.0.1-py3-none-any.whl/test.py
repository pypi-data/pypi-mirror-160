from carsomenlp.glossa import Glossa
import logging

logging.getLogger().setLevel(logging.INFO)

def test_translate():
    glossa = Glossa()
    try:
        print("Translating 'This is english'")
        print(glossa.translate("This is english"))
        
        print("Translating 'Me no hablo engles'")
        print(glossa.translate("Me no hablo engles"))
        
        logging.info("Glossa language test successful")
    except Exception as e:
        logging.error(f"Glossa language test failed on :{e}")

def test_clean():
    glossa = Glossa()
    try:
        print(f"Cleaning hondacivic")
        print(glossa.clean("hondacivic"))
        
        print(f"Cleaning proton1992")
        print(glossa.clean("proton1992"))
        
        print(f"Cleaning civic1992")
        print(glossa.clean("civic1992"))
        
        print(f"Cleaning x701992/1994")
        print(glossa.clean("x701992/1994"))
        
        print(f"Cleaning axia2.0")
        print(glossa.clean("axia2.0"))
        
        print(f"Cleaning hondasomethingg")
        print(glossa.clean("hondasomethingg"))
        
        print(f"Cleaning hondas")
        print(glossa.clean("hondas"))
        
        print(f"Cleaning protoncivic")
        print(glossa.clean("protoncivic"))
        
        logging.info("Glossa cleaning successful")
    except Exception as e:
        logging.error(f"Glossa cleaning failed on :{e}")


def test_tokenize():
    glossa =Glossa()
    try:
        print("Tokenize 'myvi 2.0 my car'")
        print(glossa.tokenize("myvi 2.0 my car"))
        logging.info("Glossa tokenize successful")
    except Exception as e:
        logging.error(f"Glossa tokenization failed on :{e}")

def test_match():
    glossa =Glossa()
    
    try:
        logging.info("Testing glossa match")
        print("Matching ", "honda civic 2.0 2009")
        print(glossa.match("honda civic 2.0 2009"))
        
        print("Matching " ,'I like axia e 1.5 manual 2022 sabah hatchback colour red')
        print(glossa.match('I like axia e 1.5 manual 2022 sabah hatchback colour red'))
        
        logging.info("Glossa match successful")
    except Exception as e:
        logging.error(f"Glossa match failed on :{e}")
        
def test_extract():
        glossa =Glossa()
        
        try:
            logging.info("Testing Glossa extract")
            print(f"Extracting produa axia e 1.5 1999 klang selangor sedan red colour")
            print(glossa.extract("produa axia e 1.5 1999 klang selangor sedan red colour"))
            logging.info("Glossa extract successful")
            print(glossa.extract("hondas"))
        except Exception as e:
            logging.error(f"Glossa extract failed on :{e}")
    
if __name__ == '__main__':
    test_translate()
    test_clean()
    test_tokenize()
    test_match()
    test_extract()
    