from django.shortcuts import render
from FitTrackPro.utils import  recs
import pandas as pd
from django.contrib.auth.decorators import login_required
from Users.models import DailyCaloriesConsumed


# Create your views here.
@login_required
def RecommendationSystem(request):
    
    #initialize dataframe
    recommendation = pd.DataFrame()
    if request.method == "POST":
        ingreds = request.POST.get('ingreds')
        recommendation = recs(ingredients=ingreds,n=10)
    return render(request ,'RecommendationSystem/RecommendationSystem.html',{"Recommendation":recommendation})