"""
Представления
"""
from django.urls import reverse_lazy
from django.views.generic import FormView

from education_app.users import create_user
from .forms import RegisterForm


class RegisterView(FormView):
    """
    Регистрация
    """
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Сохранение
        """
        data = dict(form.cleaned_data)
        about = data.pop('about')
        user_type = int(data.pop('user_type'))
        create_user(data, {'about': about}, user_type=user_type)
        return super().form_valid(form)

    def test_func(self) -> bool:
        """
        Регистрироваться может неаутентифицированный пользователь
        """
        return not self.request.user.is_authenticated
