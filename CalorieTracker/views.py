from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Users.models import UserProfile, DailyCaloriesConsumed 
import requests
from datetime import datetime, timedelta
import json
from FitTrackPro.utils import getidealcalories


now = datetime.now()
current_date = now.date()
current_time = now.time()

# Create your views here.
@login_required
def calorietracker(request):
     
    if request.method == "POST":   
        #connecting to database api and counting calories
        query = request.POST.get("food_query")
        quantity = float(request.POST.get("quantity"))
            
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        response = requests.get(api_url, headers={'X-Api-Key': '7wRMsjOOzjsTTl3iOjki6w==J0OqHjSOzvqBX74H'})
        if response.status_code == requests.codes.ok:
            data = json.loads(response.content)
            #for database
            if data == []:
                data = "Invalid Input"
                food_name = "No name"
                new_calories = 0
                carbs = 0
                protein = 0
                fat = 0
            else:
                new_calories = round((data[0]['calories'] / 100)* quantity , 2)  
                carbs =  round((data[0]['carbohydrates_total_g'] / 100)* quantity, 2)
                protein = round((data[0]['protein_g'] / 100)* quantity , 2)
                fat = round((data[0]['fat_total_g'] / 100)* quantity , 2)
                food_name = (data[0]['name'])
        else:
            error_message = "Error"
            return render(request, 'CalorieTracker/calorietracker.html', {'error_message': error_message})
        
        data_str = json.dumps(data)
        redirect_url = f'/calorietracker2/?data={data_str}&new_calories={new_calories}&carbs={carbs}&protein={protein}&fat={fat}&food_name={food_name}&quantity={quantity}'
        return redirect(redirect_url)  
               
    else:
      return render(request, 'CalorieTracker/calorietracker.html')  
    
        
@login_required
def calorietracker2(request):
    food_entries = DailyCaloriesConsumed.objects.filter(user= request.user,date = current_date).order_by('-date')
    data_str = request.GET.get('data', '{}')
    food_name = str(request.GET.get('food_name', 0))
    new_calories = float(request.GET.get('new_calories', 0))
    protein = float(request.GET.get('protein', 0))
    fat = float(request.GET.get('fat', 0))
    carbs = float(request.GET.get('carbs', 0))
    quantity = float(request.GET.get('quantity', 0))
    # Convert the data parameter from JSON to dictionary
    data = json.loads(data_str)
    if request.method =="POST":
        daily_record = DailyCaloriesConsumed(user=request.user, date=current_date, time = current_time, calories_consumed = new_calories,
                                             food_name = food_name,protein = protein,carbs = carbs, fat = fat)
        daily_record.save()
        messages.success(request, "Calories Logged Successfully")
        
        
    calories_consumed_today = 0      
    for i in food_entries:
        calories_consumed_today += i.calories_consumed
         

    return render(request,'CalorieTracker/calorietracker2.html',{'data': data, 'new_calories':new_calories,'food_entries':food_entries,
                                                                 'protein':protein,'carbs':carbs,'fat':fat,
                                                                 'calories_consumed':calories_consumed_today,
                                                                 'quantity':quantity} )    

            
@login_required
def modifyvalues(request):
    food_entries = DailyCaloriesConsumed.objects.filter(user= request.user,date = current_date).order_by('-date')
    
    calories_consumed_today = 0      
    for i in food_entries:
        calories_consumed_today += i.calories_consumed
    
    user_profile = UserProfile.objects.get(user=request.user)
    ideal_calories = getidealcalories(user_profile)   
     
    
    if request.method == "POST":
        entry_id_to_delete = request.POST.get('entry_id_to_delete')
        try:
            entry_to_delete = DailyCaloriesConsumed.objects.get(id=entry_id_to_delete)
            if entry_to_delete.user == request.user:
                entry_to_delete.delete()
                messages.success(request, 'Entry deleted successfully!')
            else:
                messages.error(request, 'You do not have permission to delete this entry.')
        except DailyCaloriesConsumed.DoesNotExist:
            messages.error(request, 'Entry not found.')
        
        redirect('modifyvalues') 
          
    return render(request, 'CalorieTracker/modifyvalues.html', {'food_entries':food_entries, 'calories_consumed':calories_consumed_today,
                                                                'ideal_calories':ideal_calories})           
   
      
        

@login_required
def dailystats(request):
    user_profile = UserProfile.objects.get(user=request.user)
    ideal_calories = getidealcalories(user_profile) 
    food_entries = DailyCaloriesConsumed.objects.filter(user=request.user, date__gte=current_date - timedelta(days=6), date__lte=current_date).order_by('date')
    
    # Calculate daily totals for the last 7 days
    daily_totals = {}
    for entry in food_entries:
        date_str = entry.date.strftime('%A')  # Get the day name 
        daily_totals.setdefault(date_str, {'protein': 0, 'carbs': 0, 'fat': 0})
        daily_totals[date_str]['protein'] += entry.protein
        daily_totals[date_str]['carbs'] += entry.carbs
        daily_totals[date_str]['fat'] += entry.fat

    # Calculate totals for the current day
    total_protein_today = sum(entry.protein for entry in food_entries.filter(date=current_date))
    total_carbs_today = sum(entry.carbs for entry in food_entries.filter(date=current_date))
    total_fat_today = sum(entry.fat for entry in food_entries.filter(date=current_date))
    calories_consumed_today = sum(entry.calories_consumed for entry in food_entries.filter(date=current_date))

    # Get the list of days and corresponding totals
    days = list(daily_totals.keys())
    protein_totals = [total['protein'] for total in daily_totals.values()]
    carbs_totals = [total['carbs'] for total in daily_totals.values()]
    fat_totals = [total['fat'] for total in daily_totals.values()]

    context = {
        'total_protein_today': total_protein_today,
        'total_carbs_today': total_carbs_today,
        'total_fat_today': total_fat_today,
        'calories_consumed_today': calories_consumed_today,
        'days': days,
        'protein_totals': protein_totals,
        'carbs_totals': carbs_totals,
        'fat_totals': fat_totals,
        'food_entries': food_entries,
        'ideal_calories':ideal_calories,
        'current_date': current_date
    }

    return render(request, 'CalorieTracker/dailystats.html', context)
    


      
'''
Mifflin-St Jeor Equation:
For men:
BMR = 10W + 6.25H - 5A + 5
For women:
BMR = 10W + 6.25H - 5A - 161
multplier :
not very active = 1.35
moderately active = 1.55
very active = 1.75 
reference: https://jcdfitness.com/2017/09/maintenance-calories/
'''