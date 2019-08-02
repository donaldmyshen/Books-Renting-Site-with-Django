from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Items, Reviews, UserBalance, UserCart, ReturnList
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import re
from decimal import Decimal


# VIEWS below:

#allow users to add money
def addMoneyForm(request):
	if request.user.is_authenticated:
		user = UserBalance.objects.get(username__username=request.user.username)
		balance = user.balance
		context = {'balance': balance}

	return render(request, 'homepage/addmoney.html', context)

#adds money to user's balance
def addMoney(request):
	amount = request.POST['add-money']
	if request.user.is_authenticated:
		user = UserBalance.objects.get(username__username=request.user.username)		
		user.balance += Decimal(amount)
		user.save()
		balance = user.balance

	context = {'balance': balance}

	return render(request, 'homepage/addmoney.html', context)

#item's details 
def detail(request, item_id):
	item = get_object_or_404(Items, pk=item_id)

	# get the user's balance
	if request.user.is_authenticated:
		user = UserBalance.objects.get(username__username=request.user.username)
		balance = user.balance
	else: 
		balance = 0

	context = {
		'item': item,
		'balance': balance
	}

	return render(request, 'homepage/detail.html', context)

def category(request):
	#get the list of items in specific category
	selected_category = request.POST['select_category']
	item_list = Items.objects.filter(category=selected_category,borrowed=False)

	if request.user.is_authenticated:
		user = UserBalance.objects.get(username__username=request.user.username)
		balance = user.balance
	else: 
		balance = 0

	# send data to template
	context = {
		'item_list': item_list,
		'balance': balance,
		'category': selected_category
	}

	return render(request, 'homepage/index.html', context)

# filter items by cost
def filtercost(request):
	maxcost = request.POST['max-cost']
	item_list = Items.objects.filter(cost__lte=Decimal(maxcost), borrowed=False)

	if request.user.is_authenticated:
		user = UserBalance.objects.get(username__username=request.user.username)
		balance = user.balance
	else: 
		balance = 0
	# context works similar with android
	context = {'item_list': item_list, 'balance': balance}
	return render(request, 'homepage/index.html', context)

# search for items
def searchItems(request):
	#get user's query, separate the words and search for them in Items table		
	query = request.GET['q']
	wordList = re.compile('([^,\s]+)').findall(query)
	item_list = []
	for word in wordList:
		tag_result = Items.objects.filter(tags__contains=word, borrowed=False)
		description_result = Items.objects.filter(description__contains=word, borrowed=False)
		name_result = Items.objects.filter(name__contains=word, borrowed=False)
		item_list += tag_result 
		item_list += name_result 
		item_list += description_result

	# deduplicate
	item_list = set(item_list)

	# get the user's balance
	if request.user.is_authenticated:
		user = UserBalance.objects.get(username__username=request.user.username)
		balance = user.balance
	else: 
		balance = 0

	context = {'item_list': item_list, 'balance': balance}
	return render(request, 'homepage/index.html', context)

#load item as lsitview, similar with android 
def ItemListView(request):

	balance = 0
	item_list = Items.objects.filter(borrowed=False)

	#get the user's balance
	if request.user.is_authenticated:
		user = UserBalance.objects.get(username__username=request.user.username)
		balance = user.balance

	context = {'item_list': item_list, 'balance': balance}
	return render(request,'homepage/index.html', context)

# load item as listview in cart, ready to check out
def cart(request):
	item_list = None
	balance = 0

	# get the items in the cart and the user's balance
	if request.user.is_authenticated:
		item_list = UserCart.objects.filter(username__username=request.user.username)
		user = UserBalance.objects.get(username__username=request.user.username)
		balance = user.balance

	context = {'item_list': item_list, 'balance': balance}
	return render(request,'homepage/cart.html', context)

# add an item to user's cart
def addCart(request, item_id):
	item = get_object_or_404(Items, pk=item_id)
	newCartItem = UserCart.objects.get_or_create(username=request.user, item=item)
	return redirect('homepage:cart')

# allows users to checkout items from their cart
def checkoutItems(request):
	cartItems = UserCart.objects.filter(username=request.user)
	sum = 0

	#find total sum of cart items
	for item in cartItems:
		sum += item.item.cost

	user = UserBalance.objects.get(username=request.user)

	#check if user have enough money
	if user.balance < sum:
		context = {'notEnoughMoney': True, 'balance': user.balance, 'item_list': cartItems}
		return render(request, 'homepage/cart.html', context)

	# checkout
	else:
		for item in cartItems:
			
			# set item as borrowed and set item owner as current user
			var = Items.objects.get(id=item.item.id)
			var.borrowed = True
			var.owner = request.user.username
			var.save()

			#update account balance of donator
			donator = UserBalance.objects.get(username=item.item.donator)
			donator.balance = donator.balance + item.item.cost
			donator.save()

		#remove the items in the cart
		cartItems.delete()

		#update user's balance
		user = UserBalance.objects.get(username=request.user)
		user.balance = user.balance - sum
		user.save()

		return redirect('homepage:profile')
# return cart
def returnB(request):
	item_list = None
	balance = 0

	# get the items in the return cart and the user's balance
	if request.user.is_authenticated:
		item_list = ReturnList.objects.filter(username__username=request.user.username)
		
		user = UserBalance.objects.get(username__username=request.user.username)
		balance = user.balance

	context = {'item_list': item_list, 'balance': balance}
	return render(request,'homepage/return.html', context)

# add an item to user's return cart 
def addReturn(request, item_id):
	item = get_object_or_404(Items, pk=item_id)
	readyReturnItem = ReturnList.objects.get_or_create(username=request.user, item=item)
	return redirect('homepage:returnB')

# allows users to return items from their return cart
def returnBooks(request):
	cartItems = ReturnList.objects.filter(username=request.user)
	sum = 0

	#find total sum of cart items
	for item in cartItems:
		sum += item.item.cost

	user = UserBalance.objects.get(username=request.user)

	for item in cartItems:
			
		# change the owner, here should be some better alogorithm but I didn't designed
		# For Lazy reason, I just set the owenr to admin
		var = Items.objects.get(id=item.item.id)
		var.borrowed = False
		var.owner = 'public'
		var.save()

		#update account balance of donator
		donator = UserBalance.objects.get(username=item.item.donator)
		donator.balance = donator.balance + item.item.cost
		donator.save()

	#remove the items in the cart
	cartItems.delete()

	#update user's balance
	user = UserBalance.objects.get(username=request.user)
	user.balance = user.balance + sum/2
	user.save()

	return redirect('homepage:profile')

# allow user check book he owned
def profile(request):
	ownedItems = Items.objects.filter(owner=request.user.username)
	balance = UserBalance.objects.get(username=request.user).balance
	context = {'item_list': ownedItems, 'balance': balance}
	return render(request, 'homepage/profile.html', context)

# add a review to an item, following forms coding idea comes from stackoverflow
class addReview(CreateView):
	model = Reviews
	fields = ['review']

	def form_valid(self, form):
		form.instance.item = Items.objects.get(id=self.kwargs['item_id'])
		form.instance.user = self.request.user
		return super(addReview, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(addReview, self).get_context_data(*args, **kwargs)
		context['balance'] = UserBalance.objects.get(username=self.request.user).balance
		return context

#creates a form for adding an item
class addItem(CreateView):
	model = Items
	fields = ['name', 'cost','description', 'image', 'category', 'tags']

	def form_valid(self, form):
		form.instance.donator = self.request.user
		form.instance.borrowed = False
		return super(addItem, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(addItem, self).get_context_data(*args, **kwargs)
		context['balance'] = UserBalance.objects.get(username=self.request.user).balance
		return context

#creates a form for editing an item
class editItem(UpdateView):
	model = Items
	fields = ['name', 'cost','description', 'image', 'category', 'tags']

	# pass data that user doesn't have to fill
	def form_valid(self, form):
		form.instance.donator = self.request.user
		form.instance.borrowed = False
		return super(editItem, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(editItem, self).get_context_data(*args, **kwargs)
		context['balance'] = UserBalance.objects.get(username=self.request.user).balance
		return context

#allows users to delete items they donate
class deleteItem(DeleteView):
	model = Items
	success_url = reverse_lazy('homepage:index')

# register
class UserRegistrationView(View):
	form_class = UserForm
	template_name = 'homepage/register.html'

	#get the form
	def get(self, request):
		emptyForm = self.form_class(None)
		context = {'form': emptyForm}
		return render(request, self.template_name, context)

	#post the form
	def post(self, request):
		filledForm = self.form_class(request.POST)

		#check if form is valid
		if (filledForm.is_valid()):
			userFormData = filledForm.save(commit=False)

			#clean up input
			username = filledForm.cleaned_data['username']
			password = filledForm.cleaned_data['password']

			#set password and save to User table
			userFormData.set_password(password)
			userFormData.save()

			#set newuser also to userbance table
			newUser = User.objects.get(username=username)
			newBalance = UserBalance(username=newUser,balance=100)
			newBalance.save()

			#auto login the user after successful registration
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('homepage:index')

		# if form is invalid, display empty form
		else:
			emptyForm = self.form_class(None)
			context = {'form': emptyForm}
			return render(request, self.template_name, context)

#log out
def logout_view(request):
	logout(request)
	item_list = Items.objects.filter(borrowed=False)
	context = {'item_list': item_list}
	return render(request,'homepage/index.html', context)

