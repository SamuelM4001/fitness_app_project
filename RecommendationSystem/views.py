from django.shortcuts import render
from FitTrackPro.utils import  recs
import pandas as pd
from django.contrib.auth.decorators import login_required
from RecommendationSystem.models import LikedRecipe
from django.contrib import messages


# Create your views here.
@login_required
def RecommendationSystem(request):
    user_liked_recipes = LikedRecipe.objects.filter(user=request.user)
    newest_liked_recipes = user_liked_recipes.order_by('-id')[:10]

# Extract ingredients from each entry
    if newest_liked_recipes != []:
        recently_liked_ingredients = [recipe.ingredients for recipe in newest_liked_recipes]
        liked_recommendations = recs(ingredients=recently_liked_ingredients,n=20)
       
    else:
        liked_recommendations = pd.DataFrame()
        
    if liked_recommendations is not None and not liked_recommendations.empty:
        liked_recipe_names = user_liked_recipes.values_list('recipe_name', flat=True)
        liked_recommendations = liked_recommendations[~liked_recommendations['Title'].isin(liked_recipe_names)]

    #initialize dataframe
    recommendation = pd.DataFrame()
    if request.method == "GET":
        if request.GET.get('action') == 'get_recs':
            ingreds = request.GET.get('ingreds')
            recommendation = recs(ingredients=ingreds,n=20)
            if recommendation is not None and not recommendation.empty:
                liked_recipe_names = user_liked_recipes.values_list('recipe_name', flat=True)
                recommendation = recommendation[~recommendation['Title'].isin(liked_recipe_names)]
    if request.method == 'POST':
        # Extract the data from the POST request
        recipe_name = request.POST.get('recipe_name')
        ingredients = request.POST.get('ingredients')
        instructions = request.POST.get('instructions')
        
        if not LikedRecipe.objects.filter(user=request.user, recipe_name=recipe_name).exists():
            # Liked recipe doesn't exist, so save it
            liked_recipe = LikedRecipe(user=request.user, recipe_name=recipe_name,
                                       ingredients=ingredients, instructions=instructions)
            liked_recipe.save()
            messages.success(request, 'Recipe added to liked recipes.')
        else:
            # Liked recipe already exists
            messages.warning(request, 'Recipe already exists in liked recipes.')
    return render(request ,'RecommendationSystem/RecommendationSystem.html',{"Recommendation":recommendation.head(10) ,
                                                                             "Liked_Recipes":newest_liked_recipes,
                                                                             "Liked_Recommendations":liked_recommendations.head(10)}) 