from django.conf.urls import url
from . import views
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'homepage'

urlpatterns = [
	#  /homepage/
	url(r'^$', views.ItemListView, name='index'),

	# /homepage/list/
	url(r'^(?P<item_id>[0-9]+)/$', views.detail, name='detail'),

	# /homepage/add
	url(r'^add/$', login_required(views.addItem.as_view()), name='add_item'),

	# /homepage/list/edit
	url(r'^(?P<pk>[0-9]+)/edit/$', login_required(views.editItem.as_view()), name='edit_item'),

	# /homepage/list/delete
	url(r'^(?P<pk>[0-9]+)/delete/$', login_required(views.deleteItem.as_view()), name='delete_item'),

	# /homepage/register
	url(r'^register/$', views.UserRegistrationView.as_view(), name='register'),

	# /homepage/logout
	url(r'^logout/$', login_required(views.logout_view), name='logout'),

	# /homepage/login
	url(r'login/$', LoginView.as_view(), name='login'),

	# /homepage/list/addReview
	url(r'^(?P<item_id>[0-9]+)/addReview/$', login_required(views.addReview.as_view()), name='add_review'),

	# /homepage/cart
	url(r'^cart/$', login_required(views.cart), name='cart'),	

	# /homepage/list/addcart
	url(r'^(?P<item_id>[0-9]+)/addcart/$', login_required(views.addCart), name='add_to_cart'),

	# /homepage/checkout
	url(r'^checkout/$', login_required(views.checkoutItems), name='checkout'),

	# /homepage/return
	url(r'^returnB/$', login_required(views.returnB), name='returnB'),	

	# /homepage/list/addreturn
	url(r'^(?P<item_id>[0-9]+)/addreturn/$', login_required(views.addReturn), name='add_to_return'),

	# /homepage/returnBooks
	url(r'^returnBooks/$', login_required(views.returnBooks), name='returnBooks'),

	# /homepage/profile
	url(r'^profile/$', login_required(views.profile), name='profile'),

	# /homepage/sort
	url(r'^sort/$', views.category, name='category'),

	# /homepage/?q=
	url(r'^search$', views.searchItems, name='search'),

	# /homepage/filtercost
	url(r'^filtercost$', views.filtercost, name='filtercost'),

	# /homepage/addmoneyform
	url(r'^addmoneyform$', views.addMoneyForm, name='addmoneyform'),

	# /homepage/addmoney
	url(r'^addmoney$', views.addMoney, name='addmoney'),

]
