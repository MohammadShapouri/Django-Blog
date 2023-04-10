from .models import UserAccount
from .forms import UserAccountForm, EditUserAccountForm, LoginForm, DeleteUserAccountForm, PasswordResetForm, EditEmailForm
from django.views.generic import CreateView, UpdateView, FormView, ListView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from blog.models import Article
from django.conf import settings
from extentions.emailVerification.EmailVerifier import EmailVerifier
from extentions.emailVerification.EmailVerifier import ActivateView, ActivateNewEmailView
from django.contrib.auth.views import (
                                    PasswordChangeView as BasePasswordChangeView,
                                    PasswordChangeDoneView as BasePasswordChangeDoneView,
                                    PasswordResetView as BasePasswordResetView,
                                    PasswordResetDoneView as BasePasswordResetDoneView,
                                    PasswordResetConfirmView as BasePasswordResetConfirmView,
                                    PasswordResetCompleteView as BasePasswordResetCompleteView
                                    )
# Create your views here.




class AddUserAccount(CreateView, EmailVerifier):
    model = UserAccount
    template_name = 'userAccount/userAccount-add.html'
    form_class = UserAccountForm
    success_url = reverse_lazy('AddUserAccount')

    account_activition_email_template = 'acc_active_email.html'
    # account_new_email_activitation_template = 'email_active_email.html'
    mail_subject = 'فعال سازی حساب جنگویی'
    email_sent_message = 'ایمیل فعال سازی حساب ارسال شد'


    def get_form_kwargs(self):
        kwargs = super(AddUserAccount, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs

    # def form_invalid(self, form):
    #     print(form.errors.as_json())
    #     return super().form_invalid(form)

    def form_valid(self, form):
        self.form = EmailVerifier.verify_email_CBV(self, self.request, form)
        return super().form_valid(form)






class ActivateUserAccount(ActivateView):
    activitation_success_message = 'موفق'
    activitation_fail_message = 'ناموفق'
    redirecting_after_activating = True
    activitation_success_template_address = 'userAccount/activitation_success_template.html'
    activitation_fail_template_address = 'userAccount/activitation_fail_template_address.html'






class EditUserAccount(LoginRequiredMixin, UpdateView):
    model = UserAccount
    template_name = 'userAccount/userAccount-edit.html'
    form_class = EditUserAccountForm
    success_url = reverse_lazy('ArticleList')

    def get_object(self):
        # pk = self.request.user.pk
        # return get_object_or_404(UserAccount, pk=pk)
        return self.request.user


    def get_form_kwargs(self):
        kwargs = super(EditUserAccount, self).get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs






class EditEmail(LoginRequiredMixin, UpdateView, EmailVerifier):
    model = UserAccount
    form_class = EditEmailForm
    template_name = 'userAccount/userAccount-edit-email.html'
    success_url = reverse_lazy('ArticleList')

    account_new_email_activitation_template = 'email_active_email.html'


    def get_object(self):
        # pk = self.request.user.pk
        # return get_object_or_404(UserAccount, pk=pk)
        return self.request.user

    def form_valid(self, form):
        self.form = EmailVerifier.verify_new_email_CBV(self, self.request, self.request.user)
        return super().form_valid(form)





class ActivateNewEmail(ActivateNewEmailView):
    activitation_success_message = 'موفق'
    activitation_fail_message = 'ناموفق'
    redirecting_after_activating = True
    activitation_success_template_address = 'userAccount/activitation_success_template.html'
    activitation_fail_template_address = 'userAccount/activitation_fail_template_address.html'




class Login(FormView):
    form_class = LoginForm
    template_name = 'userAccount/userAccount-login.html'
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)


    def form_valid(self, form):
        email_username = form.cleaned_data.get('email_username')
        password = form.cleaned_data.get('password')

        if str(email_username).__contains__('@'):
            email = email_username

            try:
                requestedUser = UserAccount.objects.get(email__iexact = email)
            except UserAccount.DoesNotExist:
                form.add_error('email_username', "حسابی با این ایمیل وجود ندارد.")
                return super().form_invalid(form)
            user = authenticate(self.request, email=requestedUser.email, password=password)
            if user is None:
                form.add_error('password', "رمز وارد شده نادرست است.")
                return super().form_invalid(form)
            else:
                login(self.request, user)
        else:
            username = email_username

            try:
                requestedUser = UserAccount.objects.get(username__iexact = username)
            except UserAccount.DoesNotExist:
                form.add_error('email_username', "حسابی با این نام کاربری وجود ندارد.")
                return super().form_invalid(form)

            user = authenticate(self.request, username=requestedUser.username, password=password)
            if user is None:
                form.add_error('password', "رمز وارد شده نادرست است.")
                return super().form_invalid(form)

        return super().form_valid(form)






class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('ArticleList')





class DeleteUserAccount(LoginRequiredMixin, FormView):
    template_name = 'userAccount/userAccount-login.html'
    form_class = DeleteUserAccountForm
    success_url = reverse_lazy('ArticleList')


    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        email = self.request.user.email

        user = authenticate(self.request, email=email, password=password)
        if user is None:
            form.add_error('password', "رمز وارد شده نادرست است.")
            return super().form_invalid(form)
        else:
            user.delete()

        return super().form_valid(form)




# class UserAccountProfile(LoginRequiredMixin, ListView):
#     model = UserAccount
#     template_name = 'userAccount/userAccount-profile.html'

#     def get_object(self):
#         return get_object_or_404(UserAccount, pk=self.request.user.pk)


class UserAccountProfile(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'userAccount/userAccount-profile.html'
    paginate_by = 8



    def get_queryset(self):
        global articleStatus
        articleStatus = self.request.GET.get('articleStatus')

        if articleStatus == 'all' or None:
            return Article.objects.filter(owner=self.request.user)
        elif articleStatus == 'p':
            return Article.objects.filter(owner=self.request.user, status='p')
        elif articleStatus == 'd':
            return Article.objects.filter(owner=self.request.user, status='d')
        elif articleStatus == 'r':
            return Article.objects.filter(owner=self.request.user, status='r')  
        else:
            return Article.objects.filter(owner=self.request.user)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userDetail'] = get_object_or_404(UserAccount, pk=self.request.user.pk)
        context['articleStatus'] = articleStatus
        return context







# next 6 views are for changing and reseting password.

class PasswordChangeView(BasePasswordChangeView):
    template_name = 'userAccount/password_change_form.html'

class PasswordChangeDoneView(BasePasswordChangeDoneView):
    template_name= 'userAccount/password_change_done.html'

class PasswordResetView(BasePasswordResetView):
    email_template_name = "userAccount/password_reset_email.html"
    form_class = PasswordResetForm
    subject_template_name = "userAccount/password_reset_subject.txt"
    template_name= 'userAccount/password_reset_form.html'

class PasswordResetDoneView(BasePasswordResetDoneView):
    template_name= 'userAccount/password_reset_done.html'

class PasswordResetConfirmView(BasePasswordResetConfirmView):
    template_name= 'userAccount/password_reset_confirm.html'

class PasswordResetCompleteView(BasePasswordResetCompleteView):
    template_name= 'userAccount/password_reset_complete.html'
