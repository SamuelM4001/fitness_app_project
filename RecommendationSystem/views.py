from django.shortcuts import render
from FitTrackPro.utils import  recs
import pandas as pd
from django.contrib.auth.decorators import login_required
from Users.models import DailyCaloriesConsumed

def title_matches_food_name(title, food_name):
    title_words = set(title.lower().split())
    return title_words.intersection(food_name)
# Create your views here.
@login_required
def RecommendationSystem(request):
    df_recipes = pd.read_csv('./FitTrackPro/datacsv/parsed_data_ftp.csv')
    food_history = DailyCaloriesConsumed.objects.filter(user=request.user).values('food_name')
    #get unique foodnames 
    food_names = set([entry['food_name'] for entry in food_history if entry['food_name'] != 'no_name'])

    list_of_ingreds = []

    for food_name in food_names:
        # Filter rows where the food_name is present in the Title
        filtered_rows = df_recipes[df_recipes['Title'].str.contains(food_name, case=False, na=False)]
        
        # Extract and concatenate all parsed ingredients for this food_name
        ingredients_list = ' '.join(filtered_rows['Parsed_Ingredients'].astype(str)).split()
        
        # Calculate the most common parsed ingredients
        common_ingredients = pd.Series(ingredients_list).value_counts().nlargest(5).index.tolist()
        list_of_ingreds.append(common_ingredients)
    
    most_common_ingredients=[]
    for i in list_of_ingreds:
        for k in range(len(i)):
            most_common_ingredients.append(i[k])
    most_common_ingredients= list(set(most_common_ingredients))       
    
    
    #initialize dataframe
    recommendation = pd.DataFrame()
    user_specific_recs =pd.DataFrame()
    if request.method == "POST":
        ingreds = request.POST.get('ingreds')
        recommendation = recs(ingredients=ingreds,data=df_recipes,n=100, picklecall=0)
        user_specific_recs = recs(ingredients=most_common_ingredients,data=recommendation,n=5,picklecall = 1)
    return render(request ,'RecommendationSystem/RecommendationSystem.html',{"Recommendation":recommendation.head(5),
                                                                             'UserRecs': user_specific_recs})