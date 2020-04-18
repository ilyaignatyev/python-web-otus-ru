"""
Представления
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView

from education_app.education import get_user_course_rights
from education_app.forms import CourseForm, CourseEntryUpdateForm, CourseEntryCreateForm, LessonForm, \
    CourseAdminCreateForm, CourseAdminUpdateForm
from education_app.models import CourseEntry, Lesson, CourseAdmin, Administrator
from education_django.settings import EMAIL_HOST_USER
from .const import USER_TYPE
from .forms import SendEmailForm
from .models import Course, Teacher, Student
from .send_email import send_email_async
from .users import get_user_type


class MyCourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Мои курсы (для студента)
    """
    model = Course
    context_object_name = 'course_entries'
    template_name = 'education_app/my_course_list.html'

    def get_queryset(self):
        """
        Возвращает queryset записей текущего пользователя-студента на курсы
        """
        return CourseEntry.objects.with_course_data.filter(student=self.request.user.id)

    def test_func(self) -> bool:
        """
        Просматривать свои курсы может только студент
        """
        return get_user_type(self.request.user.id) == USER_TYPE.STUDENT


class CourseListView(ListView):
    """
    Список курсов
    """
    model = Course
    context_object_name = 'courses'
    paginate_by = 20
    queryset = Course.objects.active


class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Создание курса
    """
    model = Course
    form_class = CourseForm

    def get_success_url(self) -> str:
        return Course.get_url(self.object.id)

    def test_func(self) -> bool:
        """
        Создавать курс может только суперпользователь
        """
        return self.request.user.is_superuser


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактирование курса
    """
    model = Course
    pk_url_kwarg = 'id'
    form_class = CourseForm

    def get_success_url(self):
        return Course.get_url(self.object.id)

    def test_func(self) -> bool:
        """
        Редактировать курс может:
        - суперпользователь
        - администратор этого курса
        """
        return Course.can_update(self.kwargs.get('id'), self.request.user)


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление курса
    """
    model = Course
    success_url = reverse_lazy('education_app:index')
    pk_url_kwarg = 'id'

    def test_func(self) -> bool:
        """
        Удалять курс может только суперпользователь
        """
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        """
        Удаление в корзину
        """
        self.object = self.get_object()
        if not self.object.deleted:
            self.object.deleted = True
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CourseView(DetailView):
    """
    Курс
    """
    model = Course
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст права текущего пользователя и идентификатор засиси на курс
        """
        context = super().get_context_data(**kwargs)
        context['rights'] = get_user_course_rights(self.request.user, self.kwargs.get('id'))

        cur_user_courseentry = CourseEntry.objects.filter(student__user__id=self.request.user.id) \
            .filter(course__id=self.kwargs.get('id')).first()
        context['cur_user_entry'] = cur_user_courseentry.id if cur_user_courseentry is not None else None

        return context


class TeacherListView(ListView):
    """
    Список преподавателей
    """
    model = Teacher
    context_object_name = 'teachers'
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(user__is_active=True).select_related('user')


class TeacherView(DetailView):
    """
    Преподаватель
    """
    model = Teacher
    pk_url_kwarg = 'id'


class StudentView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Студент
    """
    model = Student
    pk_url_kwarg = 'id'

    def test_func(self) -> bool:
        """
        Просматривать студента могут:
        - суперпользователь
        - сам студент
        - студент, администратор или преподаватель курса, на который записан студент
        """
        return Student.objects.for_user_queryset(self.request.user).filter(id=self.kwargs.get('id')).exists()


class AboutView(TemplateView):
    """
    О проекте
    """
    template_name = 'education_app/about.html'


def create_my_course_entry(request, id=None):
    """
    Запись текущего пользователя-студента на курс.
    :param request: Запрос
    :param id: Идентификатор курса
    """
    course = get_object_or_404(Course, id=id)

    student = Student.get_by_user(request.user.id)
    if student is None:
        return HttpResponseForbidden()

    if student not in course.students.all():
        CourseEntry.objects.create(course=course, student=student)
    return HttpResponseRedirect(Course.get_url(id))


class CourseEntryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Создание записи на курс
    """
    model = CourseEntry
    form_class = CourseEntryCreateForm

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def get_initial(self):
        initial = {
            'course': get_object_or_404(Course, id=self.kwargs.get('id'))
        }
        return initial

    def test_func(self) -> bool:
        """
        Создать запись на курс могут:
        - суперпользователь
        - администратор курса
        (не даем студенту записываться через эту форму, он записывается через create_my_course_entry)
        """
        if self.request.user.is_superuser:
            return True

        administrator = Administrator.get_by_user(self.request.user.id)
        if administrator is None:
            return False

        course = get_object_or_404(Course, id=self.kwargs.get('id'))
        if administrator in course.admins.all():
            return True

        return False


class CourseEntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактирование записи на курс
    """
    model = CourseEntry
    pk_url_kwarg = 'id'
    form_class = CourseEntryUpdateForm

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def test_func(self) -> bool:
        """
        Редактировать запись на курс могут:
        - суперпользователь
        - администратор курса
        """
        if self.request.user.is_superuser:
            return True

        return Course.is_admin(self.kwargs.get('id'), self.request.user.id)


class CourseEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление записи на курс
    """
    model = CourseEntry
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def test_func(self) -> bool:
        """
        Удалять запись на курс могут:
        - суперпользователь
        - администратор курса
        (студент может удалить свою запись на курс через MyCourseEntryDeleteView)
        """
        if self.request.user.is_superuser:
            return True

        return Course.is_admin(self.kwargs.get('id'), self.request.user.id)


class MyCourseEntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление записи на курс студентом
    """
    model = CourseEntry
    pk_url_kwarg = 'id'
    template_name = 'education_app/my_courseentry_confirm_delete.html'

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def test_func(self) -> bool:
        """
        Проверяем права студента
        """
        student = Student.get_by_user(self.request.user.id)
        if student is not None:
            course_entry = get_object_or_404(CourseEntry, id=self.kwargs.get('id'))
            if course_entry is not None and student in course_entry.course.students.all():
                return True

        return False


class LessonView(DetailView):
    """
    Урок
    """
    model = Lesson
    pk_url_kwarg = 'id'


class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Создание урока
    """
    model = Lesson
    form_class = LessonForm

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def get_initial(self):
        initial = {
            'course': get_object_or_404(Course, id=self.kwargs.get('id'))
        }
        return initial

    def test_func(self) -> bool:
        """
        Создавать урок могут:
        - суперпользователь
        - администратор курса, к которому относится урок
        """
        return Lesson.can_cud(self.kwargs.get('id'), self.request.user)


class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактирование урока
    """
    model = Lesson
    pk_url_kwarg = 'id'
    form_class = LessonForm

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def test_func(self) -> bool:
        """
        Редактировать урок могут:
        - суперпользователь
        - администратор курса, к которому относится урок
        """
        return Lesson.can_cud(self.kwargs.get('id'), self.request.user)


class LessonDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление урока
    """
    model = Lesson
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def test_func(self) -> bool:
        """
        Создавать урок могут:
        - суперпользователь
        - администратор курса, к которому относится урок
        """
        return Lesson.can_cud(self.kwargs.get('id'), self.request.user)


class AdministratorView(DetailView):
    """
    Администратор
    """
    model = Administrator
    pk_url_kwarg = 'id'

    def test_func(self) -> bool:
        """
        Просматривать информацию об администраторе могут:
        - суперпользователь
        - сам администратор
        - администратор, студент или преподаватель курса, на котором администратор является администратором
        """
        return Administrator.objects.for_user_queryset(self.request.user).filter(id=self.kwargs.get('id')).exists()


class CourseAdminCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Создание администратора курса
    """
    model = CourseAdmin
    form_class = CourseAdminCreateForm

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def get_initial(self):
        initial = {
            'course': get_object_or_404(Course, id=self.kwargs.get('id'))
        }
        return initial

    def test_func(self) -> bool:
        """
        Добавлять администратора курса может суперпользователь
        """
        return self.request.user.is_superuser


class CourseAdminUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Редактирование администратора курса
    """
    model = CourseAdmin
    pk_url_kwarg = 'id'
    form_class = CourseAdminUpdateForm

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def test_func(self) -> bool:
        """
        Изменять администратора курса может суперпользователь
        """
        return self.request.user.is_superuser


class CourseAdminDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление администратора курса
    """
    model = CourseAdmin
    pk_url_kwarg = 'id'

    def get_success_url(self):
        return Course.get_url(self.object.course.id)

    def test_func(self) -> bool:
        """
        Удалять администратора курса может суперпользователь
        """
        return self.request.user.is_superuser


class ContactsView(FormView):
    """
    Контакты
    """
    template_name = 'education_app/contacts.html'
    success_url = reverse_lazy('education_app:email_sent')
    form_class = SendEmailForm

    def form_valid(self, form):
        """
        Отправка сообщения
        """
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('users:login'))
        send_email_async(self.request.user, form.cleaned_data['message'], form.cleaned_data['theme'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Добавляем в контекст контактный email
        """
        context = super().get_context_data(**kwargs)
        context['contact_email'] = EMAIL_HOST_USER
        return context


class EmailSentView(TemplateView):
    """
    Сообщение отправлено
    """
    template_name = 'education_app/email_sent.html'
