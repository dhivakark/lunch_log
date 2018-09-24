from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from .forms import CustomUserCreationForm

import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
#import PyOpenSSL
import datetime
import calendar

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def get_preference(request): 
 	if request.method == 'POST':
 		now = datetime.datetime.now()
 		present_date = str(now)[:10]
 		day = now.weekday()+3
 		if 'type' in request.POST:
 			typ = request.POST.getlist('type')
 			user = request.POST.getlist('u')
 			print(typ,user)
 			gsheet(typ,user, present_date)
 			return render(request, 'pref.html', {
 			'pref':typ
 			})
 		print("posted")
 		#if 'pc' in request.POST:
 		if day == 3:
 			empc = request.POST.getlist('pc')
 			user = request.POST.getlist('u')
 			print(empc,user)
 			gsheet(empc,user, present_date)
 			if empc[0] == 'No/':
 				return render(request, 'pref.html', {
 				'pref':empc
 				})

 			return render(request, 'pref-wed.html', {
 			'pref':empc
 			})
 		empc = request.POST.getlist('pc')
 		user = request.POST.getlist('u')
 		print(empc,user)
 		gsheet(empc,user , present_date)
 		return render(request, 'pref.html', {
 		'pref':empc
 		})
 	return render(request, 'pref.html', {
 		'pref':'no choice'
 		})

def gsheet_authentication():
	json_key = json.load(open('user/creds.json')) # json credentials you downloaded earlier
	scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) 
	file = gspread.authorize(credentials) # authenticate with Google
	sheet = file.open("MUO_Python_Sheet") # open sheet
	worksheet = sheet.sheet1
	return worksheet

def gsheet(choice, user , present_date):
	worksheet = gsheet_authentication()
	choice = choice[0].rstrip('/')
	user = user[0].rstrip('/')
	all_cells = worksheet.range('A1:A11')
	all_dates = worksheet.range('B1:J1')
	count_user = 0
	count_date = 0
	for cell in all_cells:
		count_user += 1
		if cell.value == user:
			for date in all_dates:
				count_date += 1
				if date.value == present_date:
					print(chr(ord('A') + count_date)+str(count_user))
					worksheet.update_acell(chr(ord('A') + count_date)+str(count_user), choice)
