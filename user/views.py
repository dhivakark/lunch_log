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
 		day = now.weekday()
 		if 'type' in request.POST:
 			typ = request.POST.getlist('type')
 			t = typ[0].split(',')
 			gsheet(t[0], t[1], present_date)
 			return render(request, 'pref.html', {
 			'pref':typ
 			})
 		if 'c' in request.POST:
 			typ = request.POST.getlist('c')
 			t = typ[0].split(',')
 			print(t[0])
 			if day == 1:
 				return render(request, 'pref-wed.html')
 			else:
 				return render(request, 'pref-other.html')
 		
 	return render(request, 'pref.html', {
 		'pref':'no choice'
 		})
 	



def gsheet_authentication():
	json_key = json.load(open('user/config/creds.json')) # json credentials you downloaded earlier
	scope = ['https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive']
	credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope) 
	file = gspread.authorize(credentials) # authenticate with Google
	sheet = file.open("MUO_Python_Sheet") # open sheet
	worksheet = sheet.sheet1
	return worksheet

def gsheet(choice, user , present_date):
	worksheet = gsheet_authentication()
	choice = choice.rstrip('/')
	user = user.rstrip('/')
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
