from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from .forms import CustomUserCreationForm

#import logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials

import datetime
import calendar

def gsheet_authentication():
	json_key = json.load(open('user/config/creds.json')) # json credentials you downloaded earlier
	scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) 
	file = gspread.authorize(credentials) # authenticate with Google
	sheet = file.open("MUO_Python_Sheet") # open sheet
	worksheet = sheet.sheet1
	return worksheet


WORKSHEET = gsheet_authentication()

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
def get_preference(request): 
 	
 	if request.method == 'POST':
 		now = datetime.datetime.now()
 		present_date = str(now)[:10]
 		day = now.weekday()
 		if 'type' in request.POST:
 			typ = request.POST.getlist('type')
 			t = typ[0].split(',')
 			gsheet(t[0], t[1], present_date)
 			return render(request, 'pref.html', {
 			'pref':typ
 			})
 		if 'c' in request.POST:
 			if not isholiday(present_date):
 				if day == 2:
 					#logging.debug(isholiday(present_date))
 					return render(request, 'pref-wed.html')
 				else:
 					return render(request, 'pref-other.html')
 			else:
 				return render(request, 'holiday.html')
 	return render(request, 'pref.html', {
 		'pref':'no choice'
 		})
 	

def isholiday(present_date):
	worksheet = WORKSHEET
	count_date = 0
	all_dates = worksheet.range('B1:P1')
	for date in all_dates:
		count_date += 1
		if date.value == present_date:
			#logging.debug(worksheet.acell(str(chr(ord('A') + count_date)+'2')))
			if worksheet.acell(str(chr(ord('A') + count_date)+'2')).value == 'h':
				return 1
			else:
				return 0



def gsheet(choice, user , present_date):
	worksheet = WORKSHEET
	all_cells = worksheet.range('A1:A11')
	all_dates = worksheet.range('B1:P1')
	count_user = 0
	count_date = 0
	for cell in all_cells:
		count_user += 1
		if cell.value == user:
			for date in all_dates:
				count_date += 1
				if date.value == present_date:
					#logging.debug(chr(ord('A') + count_date)+str(count_user))
					worksheet.update_acell(chr(ord('A') + count_date)+str(count_user), choice)

def weekly_entry(request):
	if request.method == 'POST':
		global name
		name = request.POST['name']
		worksheet = WORKSHEET
		now = datetime.datetime.now()
		present_date = str(now)[:10]
		day = now.weekday()
		all_dates = worksheet.range('B1:P1')
		global date_list
		date_list = list()
		count_date = 0
		count_user = 0
		all_cells = worksheet.range('A1:A11')
		for cell in all_cells:
			count_user += 1
			if cell.value == name:
				for date in all_dates:
					count_date += 1
					if date.value == present_date or 0<len(date_list)<6:
						column = chr(ord('A') + count_date)
						if worksheet.acell(str(column+'2')).value == 'w':
							choice = worksheet.acell(str(column+str(count_user))).value
							date_list.append([date.value, day%7, choice])
						day += 1
					if len(date_list) > 5:
						break
				break
		context={'week_list':date_list}
		return render(request, 'weekly_log.html',context)

def week_updated(request):
	'''
   	call the function weekly_entry and get the value of date_list and name 
   	by returning it when if condition to evaluate request whether it is post or not fails
	''' 
	if request.method == "POST":
		for date in date_list:
			choice = request.POST[date[0]]
			choice = choice.split(',')
			if choice[0] != choice[1]:
				gsheet(choice[0], name , date[0])
	return render(request, 'pref.html')	












