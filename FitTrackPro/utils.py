import pandas as pd
import nltk
import string
import re
import unidecode
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import pickle
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer



'''RECOMMENDATION SYSTEM FUNCTIONS P1'''
#INGREDIENT PARSER FUNCTION
def ingredient_parser(ingreds):
    measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', 'tbl.', 'tb', 'tbsp.', 'fluid ounce', 'fl oz', 'gill', 'cup', 'c', 'pint', 'p', 'pt', 'fl pt',
                'quart', 'q', 'qt', 'fl qt', 'gallon', 'g', 'gal', 'ml', 'milliliter', 'millilitre', 'cc', 'mL', 'l', 'liter', 'litre', 'L', 'dl', 'deciliter',
                'decilitre', 'dL', 'bulb', 'level', 'heaped', 'rounded', 'whole', 'pinch', 'medium', 'slice', 'pound', 'lb', '#', 'ounce', 'oz', 'mg', 'milligram',
                'milligramme', 'g', 'gram', 'gramme', 'kg', 'kilogram', 'kilogramme', 'x', 'of', 'mm', 'millimetre', 'millimeter', 'cm', 'centimeter', 'centimetre',
                'm', 'meter', 'metre', 'inch', 'in', 'milli', 'centi', 'deci', 'hecto', 'kilo']
    
    words_to_remove = ['fresh', 'oil', 'a', 'red', 'bunch', 'and', 'clove', 'or', 'leaf', 'chilli', 'large', 'extra', 'sprig', 'ground', 'handful', 'free',
                       'small', 'pepper', 'virgin', 'range', 'from', 'dried', 'sustainable', 'black', 'peeled', 'higher', 'welfare', 'seed', 'for', 'finely',
                       'freshly', 'sea', 'quality', 'white', 'ripe', 'few', 'piece', 'source', 'to', 'organic', 'flat', 'smoked', 'ginger', 'sliced', 'green',
                       'picked', 'the', 'stick', 'plain', 'plus', 'mixed', 'mint', 'bay', 'basil', 'your', 'cumin', 'optional', 'fennel', 'serve', 'mustard', 
                       'unsalted', 'baby', 'paprika', 'fat', 'ask', 'natural', 'skin', 'roughly', 'into', 'such', 'cut', 'good', 'brown', 'grated', 'trimmed',
                       'oregano', 'powder', 'yellow', 'dusting', 'knob', 'frozen', 'on', 'deseeded', 'low', 'runny', 'balsamic', 'cooked', 'streaky', 'nutmeg', 
                       'sage', 'rasher', 'zest', 'pin', 'groundnut', 'breadcrumb', 'turmeric', 'halved', 'grating', 'stalk', 'light', 'tinned', 'dry', 'soft', 
                       'rocket', 'bone', 'colour', 'washed', 'skinless', 'leftover', 'splash', 'removed', 'dijon', 'thick', 'big', 'hot', 'drained', 'sized', 
                       'chestnut', 'watercress', 'fishmonger', 'english', 'dill', 'caper', 'raw', 'worcestershire', 'flake', 'cider', 'cayenne', 'tbsp', 'leg',
                       'pine', 'wild', 'if', 'fine', 'herb', 'almond', 'shoulder', 'cube', 'dressing', 'with', 'chunk', 'spice', 'thumb', 'garam', 'new', 'little',
                       'punnet', 'peppercorn', 'shelled', 'saffron', 'other''chopped', 'salt', 'olive', 'taste', 'can', 'sauce', 'water', 'diced', 'package', 'italian',
                       'shredded', 'divided', 'parsley', 'vinegar', 'all', 'purpose', 'crushed', 'juice', 'more', 'coriander', 'bell', 'needed', 'thinly', 'boneless',
                       'half', 'thyme', 'cubed', 'cinnamon', 'cilantro', 'jar', 'seasoning', 'rosemary', 'extract', 'sweet', 'baking', 'beaten', 'heavy', 'seeded', 'tin',
                       'vanilla', 'uncooked', 'crumb', 'style', 'thin', 'nut', 'coarsely', 'spring', 'chili', 'cornstarch', 'strip', 'cardamom', 'rinsed', 'honey', 'cherry',
                       'root', 'quartered', 'head', 'softened', 'container', 'crumbled', 'frying', 'lean', 'cooking', 'roasted', 'warm', 'whipping', 'thawed', 'corn', 
                       'pitted','sun', 'kosher', 'bite', 'toasted', 'lasagna', 'split', 'melted', 'degree', 'lengthwise', 'romano', 'packed', 'pod', 'anchovy', 'rom',
                       'prepared', 'juiced','fluid', 'floret', 'room', 'active', 'seasoned', 'mix', 'deveined', 'lightly', 'anise', 'thai', 'size', 'unsweetened',
                       'torn', 'wedge', 'sour', 'basmati','marinara', 'dark', 'temperature', 'garnish', 'bouillon', 'loaf', 'shell', 'reggiano', 'canola', 'parmigiano',
                        'round', 'canned', 'ghee', 'crust', 'long', 'broken', 'ketchup', 'bulk', 'cleaned', 'condensed', 'sherry', 'provolone', 'cold', 'soda',
                        'cottage', 'spray', 'tamarind', 'pecorino', 'shortening', 'part', 'bottle', 'sodium', 'cocoa', 'grain', 'french', 'roast', 'stem', 'link',
                        'firm', 'asafoetida', 'mild', 'dash', 'boiling','ADVERTISEMENT', 'advertisement', 'chopped', 'only', 'minced']
    
    if isinstance(ingreds, list):
        ingredients = ingreds
    else:
        ingredients = re.split(r'\s|,', ingreds)
        
    translator = str.maketrans('', '', string.punctuation)
    lemmatizer = WordNetLemmatizer()
    ingred_list = []
    
    for i in ingredients:
        i = i.translate(translator)
        # We split up with hyphens as well as spaces
        items = re.split(' |-', i)
        # Get rid of words containing non alphabet letters
        items = [word for word in items if word.isalpha()]
        # Turn everything to lowercase
        items = [word.lower() for word in items]
        # remove accents
        items = [unidecode.unidecode(word) for word in items] #''.join((c for c in unicodedata.normalize('NFD', items) if unicodedata.category(c) != 'Mn'))
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # Gets rid of measuring words/phrases, e.g. heaped teaspoon
        items = [word for word in items if word not in measures]
        # Get rid of common easy words
        items = [word for word in items if word not in words_to_remove]
        if items:
            ingred_list.append(' '.join(items)) 
    ingred_list = " ".join(ingred_list)
    return ingred_list


'''RECOMMENDATION SYSTEM FUNCTIONS P2'''
#FINAL PARSER FUNCTION
def ingredient_parser_final(ingredient):
    if isinstance(ingredient, list):
        ingredients = ingredient
    else:
        # Split the string into individual ingredients
        ingredients = ingredient.split(',')
    
    ingredients = ','.join(ingredients)
    ingredients = unidecode.unidecode(ingredients)
    return ingredients

def title_parser(title):
    title = unidecode.unidecode(title)
    return title 


#RECOMMENDATION SYSTEM
    
def recs(ingredients,n):
    data = pd.read_csv('./FitTrackPro/datacsv/parsed_data_ftp.csv')
    with open('./FitTrackPro/datacsv/encoding.pickle', 'rb') as f:
            tfidf_encodings = pickle.load(f)
            
    with open('./FitTrackPro/datacsv/trained_model.pickle', "rb") as f:
            tfidf = pickle.load(f)
            
    try:
        ingredients_parsed = ingredient_parser(ingredients)
    except (ValueError, TypeError) as e:
        ingredients_parsed = ingredient_parser([ingredients])
        
    if isinstance(ingredients_parsed, str):
        ingredients_parsed = [ingredients_parsed]
        
    ingredients_tfidf = tfidf.transform(ingredients_parsed) #transforms the input according to my tfidf model
    
    knn = NearestNeighbors(n_neighbors=n, metric='cosine') #Initializes knn algorithm to find 5 nearest neighbours based on cosine similarity
    knn.fit(tfidf_encodings)
    distances, indices = knn.kneighbors(ingredients_tfidf) #applies the knn algorithm, the output has a 2d array containing the distances of the points from the input and a list containing the indices of the nearest points

    # Use a list to store recommendations
    recommendations = []

    for i in indices[0]:
        title = title_parser(data['Title'][i])
        parsed_ingredients = ingredient_parser_final(data['Parsed_Ingredients'][i])
        ingredients = title_parser(data['Ingredients'][i])
        instructions = title_parser(data['Instructions'][i])
        recommendations.append({'Title': title,'Parsed_Ingredients': parsed_ingredients ,'Ingredients': ingredients, 'Instructions': instructions})

    # Create the DataFrame from the list
    recommendation = pd.DataFrame(recommendations)
    
    #adding distances to the dataframe
    scores = [distances[0][i] for i in range(len(distances[0]))]    
    recommendation['Scores']= scores
   
    return recommendation


#finding maintainence and ideal calories 
def getidealcalories(user_profile):
    activity_level = user_profile.activity_level
    gender= user_profile.gender
    goal=user_profile.goal
    weight=user_profile.current_weight
    height=user_profile.height
    age=user_profile.age
    if activity_level == 'not_very_active':
        multiplier = 1.35
    elif activity_level == 'very_active':
        multiplier = 1.75
    else:
         multiplier = 1.55
        
    if gender == 'male':
        maintainence_calories = ((10*weight) + (6.25*height) - (5*age) + 5)*multiplier
    else:
        maintainence_calories = ((10*weight) + (6.25*height) - (5*age) - 161)*multiplier
        
    if goal == 'maintain_weight':
        ideal_calories = maintainence_calories
    elif goal =='lose_weight':
            ideal_calories = maintainence_calories - 300
    else:
        ideal_calories = maintainence_calories + 300   
    
    return ideal_calories
