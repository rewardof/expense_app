from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from account.models import User, Role, UserRole, Profile
from .forms import UserRoleCreationForm, AddExpenseForm, EditProfileForm, EditUserForm
from django.contrib import messages
from .models import UserExpense
from .filters import ExpenseFilter
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test



@login_required(login_url='/')
def index(request):
    users = User.objects.filter(family=request.user.family).exclude(username=request.user.username)
    user_list = []
    for user in users:
        obj = UserRole.objects.filter(user1=request.user, user2=user)
        if obj:
            data = {'user': user,
                    'role': obj[0].role}
        else:
            data = {'user': user,
                    'role': '-'}
        user_list.append(data)
    user1 = request.user
    image = user1.profile.image.url
    users.exclude()
    roles = Role.objects.all()
    context = {
        'users': user_list,
        'roles': roles,
        'user1': user1,
        'image': image
    }
    if request.method == 'POST':
        form = UserRoleCreationForm(data=request.POST)
        if form.is_valid():
            user1 = request.user
            user2 = form.cleaned_data['user2']
            role = form.cleaned_data['role']
            user_role, created = UserRole.objects.update_or_create(user1=user1, user2=user2, role=role)
            user_role.save()
            # context['role'] = role
            return render(request, 'expense/index.html', context)
        else:
            form = UserRoleCreationForm()
            context['form'] = form
            return render(request, 'expense/index.html', context)
    else:
        form = UserRoleCreationForm()
        context['form'] = form
        return render(request, 'expense/index.html', context)


@login_required(login_url='/')
def add_expense(request):
    form = AddExpenseForm()
    if request.method == 'POST':
        items = request.POST['items']
        cost = request.POST['cost']
        category = request.POST['category']
        description = request.POST['description']
        if not items:
            messages.error(request, 'Items field is required')
        if not cost:
            messages.error(request, 'Cost field is required')
        if not category:
            messages.error(request, 'Category field is required')
        expense1 = UserExpense.objects.create(user=request.user, items=items, cost=cost, category=category,
                                              description=description)
        expense1.save()
        messages.success(request, 'Expense is created successfully')
        return redirect('expense:expenses_list')
    else:
        context = {
            'form': form
        }
        return render(request, 'expense/add_expense.html', context)

    # TODO in future this should be implemented


# def family_members_list(request):
#     user = request.user
#     members = User.objects.filter(family=user.family)
#     context = {
#         "members": members
#     }
#     return render(request, )


# def user_has_permission(user):
#     return user.has_perm('expense.can_view_expenses')
# @permission_required('expense.can_view_expenses', login_url='/')
# @user_passes_test(lambda u: u.has_perm('expense.can_view_expenses'))


@login_required(login_url='/')
@permission_required('expense.can_view_expenses', raise_exception=True)
def family_expense_list(request, member_id):
    expenses = UserExpense.objects.filter(user_id=member_id).order_by('-date_added')
    expenses = expenses
    context = {
        "expenses": expenses,
        'user': request.user,
    }
    return render(request, 'expense/member_expenses.html', context=context)


@login_required(login_url='/register/')
def expenses_list_view(request):
    expenses = UserExpense.objects.filter(user=request.user).order_by('-date_added')
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword', None)
        if keyword:
            expenses = expenses.filter(Q(items__icontains=keyword) | Q(category__icontains=keyword) |
                                       Q(description__icontains=keyword))
    total_expense = 0
    for expense in expenses:
        total_expense += expense.cost
    myfilter = ExpenseFilter(request.GET, queryset=expenses)
    expenses = myfilter.qs
    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'myfilter': myfilter,

    }
    return render(request, 'expense/expenses_list.html', context)


@login_required(login_url='/')
def update_expense_view(request, expense_id):
    expense = UserExpense.objects.get(id=expense_id)
    form = AddExpenseForm(instance=expense)
    if request.method == "POST":
        form = AddExpenseForm(request.POST or None, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense is updated successfully')
            return redirect('expense:expenses_list')
    context = {
        'form': form,
        'expense_id': expense_id
    }
    return render(request, 'expense/update_expense.html', context)


@login_required(login_url='/')
def profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is successfully updated')
            return redirect('expense:home')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'profile/edit_profile.html', context)
