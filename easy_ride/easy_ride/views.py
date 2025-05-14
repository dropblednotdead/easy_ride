from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView

from easy_ride.forms import RegistrationUserForm, AuthorizationUserForm, UserInformationForm
from easy_ride.models import Reviews, Categories, Sales, UserInformation, Cars, Brand

from django.contrib import messages
from .models import Cars, Rent
from .forms import RentForm
# Create your views here.


def main_page(request):
    reviews = Reviews.objects.filter(is_published=True).order_by('-date')[:3]
    categories = Categories.objects.filter(pk__lt=4)
    sales = Sales.objects.filter(end_date__gt=timezone.now())
    published_reviews = Reviews.objects.filter(is_published=True).order_by('-date')[:5]
    rents = Rent.objects.filter(client=request.user.user_info)
    context = {
        'reviews': reviews,
        'categories': categories,
        'sales': sales,
        'published_reviews': published_reviews,
        'rents': rents,
    }
    return render(request, 'easy_ride/main.html', context)


class RegistrationUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'easy_ride/registration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class AuthorizationUser(LoginView):
    form_class = AuthorizationUserForm
    template_name = 'easy_ride/authorization.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('main')


@login_required
def user_profile_view(request):
    try:
        user_info = request.user.user_info
    except UserInformation.DoesNotExist:
        user_info = None

    edit_mode = request.GET.get('edit') == 'true' or user_info is None
    if request.method == 'POST':
        form = UserInformationForm(request.POST, request.FILES, instance=user_info)
        if form.is_valid():
            user_info = form.save(commit=False)
            user_info.user = request.user
            user_info.save()
            return redirect('user')
    else:
        form = UserInformationForm(instance=user_info)

    return render(request, 'easy_ride/profile.html', {
        'form': form,
        'user_info': user_info,
        'edit_mode': edit_mode,
    })


class CategoriesPage(ListView):
    paginate_by = 3
    model = Categories
    template_name = "easy_ride/categories.html"
    context_object_name = "categories"


class CategoryPage(ListView):
    paginate_by = 3
    model = Cars
    template_name = "easy_ride/category.html"
    context_object_name = "cars"

    def get_queryset(self):
        category = self.kwargs.get('category')
        return Cars.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def rent_car(request, pk):
    car = get_object_or_404(Cars, pk=pk)

    if not car.is_free:
        if Rent.objects.get(car=car).end_date < timezone.now():
            car.is_free = True
            car.save()
        else:
            messages.error(request, "Этот автомобиль сейчас занят и недоступен для аренды")
            return render(request, 'easy_ride/rent.html', {'car': car, 'not_available': True})

    if request.method == 'POST':
        form = RentForm(request.POST)
        if form.is_valid():
            rent = form.save(commit=False)
            rent.car = car
            rent.client = request.user.user_info
            rent.save()

            # Помечаем машину как занятую
            car.is_free = False
            car.save()

            messages.success(request, "Заявка на аренду успешно создана! Ожидайте подтверждения.")
            return redirect('profile', pk=car.pk)
    else:
        form = RentForm()

    return render(request, 'easy_ride/rent.html', {
        'form': form,
        'car': car,
        'not_available': False
    })


class MyRentsPage(ListView):
    paginate_by = 1
    model = Rent
    template_name = "easy_ride/rents.html"
    context_object_name = "rents"

    def get_queryset(self):
        user_info = self.request.user.user_info
        return Rent.objects.filter(client=user_info)


class SalesPage(ListView):
    paginate_by = 3
    model = Sales
    template_name = "easy_ride/sales.html"
    context_object_name = "discounts"


def create_review(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            review = Reviews(
                message=message,
                client=request.user.user_info if hasattr(request.user, 'user_info') else None,
                is_published=False  # По умолчанию отзыв не опубликован
            )
            review.save()
            messages.success(request, 'Спасибо за ваш отзыв! Он будет опубликован после проверки.')
            return redirect('main')  # Замените 'main' на имя вашего URL главной страницы
        else:
            messages.error(request, 'Пожалуйста, напишите отзыв перед отправкой.')

    return render(request, 'easy_ride/review.html')