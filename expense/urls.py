from django.urls import path

from . import views

app_name = 'expense'
urlpatterns = [
    path('', views.index, name='home'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expenses_list/', views.expenses_list_view, name='expenses_list'),
    path('update_expense/<int:expense_id>/', views.update_expense_view, name='update_expense'),
    path('edit_profile/', views.profile, name='edit_profile'),
    path('family-expense-list/<int:member_id>/', views.family_expense_list, name='family_expense_list')
]
