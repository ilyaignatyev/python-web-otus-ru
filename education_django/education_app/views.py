"""
Представления
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from education_app.education import lesson_cud_rights, get_user_course_rights
from education_app.forms import CourseForm, CourseEntryUpdateForm, CourseEntryCreateForm, LessonForm, \
    CourseAdminCreateForm, CourseAdminUpdateForm
from education_app.models import CourseEntry, Lesson, CourseAdmin, Administrator
from .models import Course, Teacher, Student


class MyCourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Мои курсы (для студента)
    """
    model = Course
    context_object_name = 'course_entries'
    template_name = 'education_app/my_course_list.html'

    def get_queryset(self):
        return CourseEntry.objects.filter(student=self.request.user.id)

    def test_func(self) -> bool:
        """
        Просматривать свои курсы может только студент
        """
        return Student.get_by_user(self.request.user.id) is not None


class CourseListView(ListView):
    """
    Список курсов
    """
    model = Course
    context_object_name = 'courses'
    paginate_by = 2

    def get_queryset(self):
        return self.model.objects.filter(deleted=False)


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
        Создавать курс может только администратор системы
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
        - администратор системы
        - администратор курса
        """
        if self.request.user.is_superuser:
            return True

        administrator = Administrator.get_by_user(self.request.user.id)
        if administrator is not None:
            course = get_object_or_404(Course, id=self.kwargs.get('id'))
            if administrator in course.admins.all():
                return True
        return False


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Удаление курса
    """
    model = Course
    success_url = reverse_lazy('education_app:index')
    pk_url_kwarg = 'id'

    def test_func(self) -> bool:
        """
        Удалять курс может только администратор системы
        """
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
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
    paginate_by = 2

    def get_queryset(self):
        return self.model.objects.filter(user__is_active=True)


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
        Просматривать стдудента могут:
        - администратор системы
        - сам студент
        - администратор курса, на который записан студент
        - преподаватель курса, на который записан студент
        """
        if self.request.user.is_superuser:
            return True

        student_obj = get_object_or_404(Student, id=self.kwargs.get('id'))
        if student_obj.user == self.request.user:
            return True

        administrator = Administrator.get_by_user(self.request.user.id)
        if administrator is not None:
            return Course.objects.filter(courseentry__student__id=student_obj.id). \
                filter(courseadmin__admin__id=administrator.id).exists()

        teacher = Teacher.get_by_user(self.request.user.id)
        if teacher is not None:
            return Course.objects.filter(courseentry__student__id=student_obj.id). \
                filter(lesson__teacher__id=teacher.id).exists()

        return False


def about(request):
    """
    О проекте
    """
    return render(request, 'education_app/about.html')


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
        - администратор системы
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
        - администратор системы
        - администратор курса
        """
        if self.request.user.is_superuser:
            return True

        administrator = Administrator.get_by_user(self.request.user.id)
        if administrator is not None:
            course = get_object_or_404(Course, id=self.kwargs.get('id'))
            if administrator in course.admins.all():
                return True

        return False


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
        - администратор системы
        - администратор курса
        (студент может удалить свою запись на курс через MyCourseEntryDeleteView)
        """
        if self.request.user.is_superuser:
            return True

        administrator = Administrator.get_by_user(self.request.user.id)
        if administrator is not None:
            course = get_object_or_404(Course, id=self.kwargs.get('id'))
            if administrator in course.admins.all():
                return True

        return False


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
        - администратор системы
        - администратор курса
        """
        return lesson_cud_rights(self.request.user, self.kwargs.get('id'))


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
        - администратор системы
        - администратор курса
        """
        return lesson_cud_rights(self.request.user, self.kwargs.get('id'))


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
        - администратор системы
        - администратор курса
        """
        return lesson_cud_rights(self.request.user, self.kwargs.get('id'))


class AdministratorView(DetailView):
    """
    Администратор
    """
    model = Administrator
    pk_url_kwarg = 'id'


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
        Добавлять администратора курса может администратор системы
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
        Изменять администратора курса может администратор системы
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
        Удалять администратора курса может администратор системы
        """
        return self.request.user.is_superuser
