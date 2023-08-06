import re
from carsomenlp.utils import load_lib,load_json_lib

# MB_LIB = load_json_lib("src/carsomenlp/artefacts/model_brand.json")
BM_LIB = load_json_lib("src/carsomenlp/artefacts/brand_model.json")

def fix_brand(text: str):
        """auxiliary method to fix and standardize car brand name

        Args:
        text (str): car brand name

        Returns:
        str: returning the same car brand in standrad format
        """
        cleanup_list = {'bwm': 'bmw',
                        'bnw': 'bmw',
                        'lambo': 'lamboghini',
                        'merz': 'mercedes',
                        'mercedez': 'mercedes',
                        'merc': 'mercedes',
                        'amg': 'mercedes',
                        'benz': 'mercedes',
                        'bezn': 'mercedes',
                        'benze': 'mercedes',
                        'banz': 'mercedes',
                        'bens': 'mercedes',
                        'ben': 'mercedes',
                        'mbenz': 'mercedes',
                        'vw': 'volkswagen',
                        'volk': 'volkswagen',
                        'chev': 'chevrolet',
                        'izusu': 'isuzu',
                        'izuzu': 'isuzu',
                        'toyo': 'toyota',
                        'aston': 'aston martin',

                        'masda': 'mazda',
                        'mercides': 'mercedes',
                        'mercidez': 'mercedes',
                        'citreon': 'citroen',
                        'citron': 'citroen',
                        'dahatsu': 'daihatsu',
                        'hyudai': 'hyundai',
                        'mitshubishi': 'mitsubishi',
                        'perduo': 'perodua',
                        'produa': 'perodua',
                        'pegeout': 'peugeot',
                        'porshe': 'porsche',
                        'toyata': 'toyota',
                        'volkwagen': 'volkswagen',

                        'at': 'auto',
                        'mt': 'manual',

                        '4x4': 'truck',
                        'four-wheel': 'truck',

                        'kl': 'kuala lumpur'
                        }
        for wrong_word, correct_word in cleanup_list.items():
                text = re.sub(r'\b' + wrong_word + r'\b', correct_word, text)

        return text


def clean_space(text):
    """Text cleaning process

    Args:
            text (str): string query

    Returns:
            str: cleaned string query
    """
    text = re.sub('\s+', ' ', text)
    text = text.strip()
    return text


def fix_space(text):
    """auxiliary method to fix car brand and model names using regular expression. Adding space to split car brand and model or engine.

    Args:
            text (_type_): a string/sentence that might inlcude brand and model name
            brand_lib (_type_, optional): _description_. Defaults to imported_brand_binaries.
            model_lib (_type_, optional): _description_. Defaults to imported_model_binaries.
            regulate_brands (bool, optional): _description_. Defaults to True.
            regulate_models (bool, optional): _description_. Defaults to True.

    Returns:
            _type_: _description_
    """
    year_re = '((198|199|200|201|202|203|204)(\d{1})/?){1,2}'
    engine_re = '(\d\.\d)'
    matched = " \g<1> \g<2>"
    
    for brand, models in BM_LIB.items():
        bm_re = rf"({brand})({'|'.join(models)})"
        text = re.sub(bm_re, matched, text)
        
        #brand inclusiv
        bm = [brand]+models
        bm_re = rf"({'|'.join(bm)})"
        reg_year_re = rf"{bm_re}{year_re}"
        text = re.sub(reg_year_re, matched, text)
        
        reg_engine_re = rf"{bm_re}{engine_re}"
        text = re.sub(reg_engine_re, matched, text)
        

    return clean_space(text)
