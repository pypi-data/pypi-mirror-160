import spacy
from spacy.matcher import Matcher
from rapidfuzz import process
from rapidfuzz.string_metric import normalized_levenshtein
from rapidfuzz.string_metric import jaro_winkler_similarity

from carsomenlp.utils import load_lib, load_json_lib


# Library loading
MB_LIB = load_json_lib("src/carsomenlp/artefacts/model_brand.json")
BM_LIB = load_json_lib("src/carsomenlp/artefacts/brand_model.json")
MODEL_LIB = sorted(load_lib("src/carsomenlp/artefacts/model_lib.npy"), key=len, reverse=True)
BRAND_LIB = sorted(load_lib("src/carsomenlp/artefacts/brand_lib.npy"), key=len, reverse=True)


# Initialize matcher
nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)

PATTERNS = load_json_lib("src/carsomenlp/artefacts/patterns.json")
    
for key, pattern in PATTERNS.items():
    matcher.add(key, [pattern], greedy='LONGEST')
    
def exact_match(doc):
    """ Find exact string match for BMYTETM

    Args:
        doc (doc): spacy doc

    Returns:
        dict: dictionary of matched items
    """
    
    matches = matcher(doc)
    matched = { key:None for key in PATTERNS.keys()}

    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        if matched[string_id] == None:
            matched[string_id] = span.text
        
        # LONGEST matching
        if len(matched[string_id]) < len(span.text):
            matched[string_id] = span.text
        
    return matched    

def fuzzy_match(tokens, items,jaro_threshold = 90, levenshtein_threshold=80):
    """ Match tokens in items with longest string with top priority

    Args:
        tokens (list): list of keywords seperated from text
        items (list): list if items for fuzzy to compare to
        jaro_threshold (int, optional): The value to filter jaro fuzzy. Defaults to 90.
        levenshtein_threshold (int, optional): The value to filter levenshtein fuzzy. Defaults to 80.

    Returns:
        _type_: _description_
    """
    matched = []
    for token in tokens:
        # Match car model
        to_match = str(token)
        fuzz_result = process.extractOne(to_match, items, scorer=jaro_winkler_similarity)

        # Store results and remove found words.
        if fuzz_result[1] > jaro_threshold:
            matched.append(fuzz_result)
        else:
            fuzz_result = process.extractOne(to_match, items, scorer=normalized_levenshtein)
            
            if fuzz_result[1] >= levenshtein_threshold:
                matched.append(fuzz_result)
                
    # Get string and sort by len des
    matched = [str(res[0]) for res in matched]
    if len(matched) > 0:
        matched = sorted(matched, key=len, reverse=True)[0]
        return matched
    
    

def fuzzy_match_brand_model(matches, tokens):
    """ Matched brand or model exist in library with fuzzy

    Args:
        matches (dict): list of matched keys
        tokens (list): chunks of text keywords

    Returns:
        dict: updated matched dictionary
    """
    
    # Assisted by brand / model respectively, MB wrapped in list because kv for MB is direct string
    
    brand_items = BRAND_LIB if matches['model'] is None else MB_LIB[matches['model']]
    # Brand
    if matches['brand'] is None:
        brand_matched = fuzzy_match(tokens, brand_items)
        matches['brand'] = brand_matched
        
    model_items = MODEL_LIB if matches['brand'] is None else BM_LIB[matches['brand']]
    
    # Model
    if matches['model'] is None:
        model_matched = fuzzy_match(tokens, model_items)
        matches['model'] = model_matched
    
        
    # Inferred brand from model
    if matches['brand'] is None and matches['model'] is not None and matches['model'] in MB_LIB:
        # returning first
        matches['brand'] = MB_LIB[matches['model']][0]
    return matches
