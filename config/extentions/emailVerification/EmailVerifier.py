from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .TokenGenerator import account_activation_token  
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic import View




class EmailVerifier():
    account_activition_email_template = None
    account_new_email_activitation_template = None
    mail_subject = None
    showing_message_after_sending_email = True
    email_sent_message = 'Please confirm your email address to complete the registration.'



    def verify_email_CBV(self, request, form):
        # save form in the memory not in database  
        user = form.save(commit=False)  
        user.is_active = False
        user.save()

        # to get the domain of the current site  
        current_site = get_current_site(request)  
        # mail_subject = 'Activation link has been sent to your email id' 
        message = render_to_string(self.account_activition_email_template, { 
            'user': user,  
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
            'token':account_activation_token.make_token(user),  
        })
        to_email = form.cleaned_data.get('email')  
        email = EmailMessage(
                    self.mail_subject, message, to=[to_email]  
        )  
        email.send()

        if self.showing_message_after_sending_email:
            if isinstance(self.email_sent_message, str) or isinstance(self.email_sent_message, int):
                messages.add_message(request, messages.SUCCESS, self.email_sent_message)
            else:
                messages.add_message(request, messages.SUCCESS, 'Please confirm your email address to complete the registration')
        return user





    def verify_new_email_CBV(self, request, user):
        # to get the domain of the current site  
        current_site = get_current_site(request)  
        # mail_subject = 'Activation link has been sent to your email id' 
        message = render_to_string(self.account_new_email_activitation_template, { 
            'user': user,  
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
            'token':account_activation_token.make_token(user),
        })
        to_email = user.new_email
        email = EmailMessage(
                    self.mail_subject, message, to=[to_email]
        )  
        email.send()

        if self.showing_message_after_sending_email:
            if isinstance(self.email_sent_message, str) or isinstance(self.email_sent_message, int):
                messages.add_message(request, messages.SUCCESS, self.email_sent_message)
            else:
                messages.add_message(request, messages.SUCCESS, 'Please confirm your email address to complete the registration')
        return user





    # def base_email_verifier_CBV(self, request, form):
    #     # save form in the memory not in database  
    #     user = form.save(commit=False)  
    #     user.save()

    #     # to get the domain of the current site  
    #     current_site = get_current_site(request)  
    #     # mail_subject = 'Activation link has been sent to your email id' 
    #     message = render_to_string(self.account_new_email_activitation_template, { 
    #         'user': user,  
    #         'domain': current_site.domain,
    #         'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
    #         'token':account_activation_token.make_token(user),  
    #     })
    #     to_email = form.cleaned_data.get('email')  
    #     email = EmailMessage(
    #                 self.mail_subject, message, to=[to_email]  
    #     )  
    #     email.send()

    #     if self.showing_message_after_sending_email:
    #         if isinstance(self.email_sent_message, str) or isinstance(self.email_sent_message, int):
    #             messages.add_message(request, messages.SUCCESS, self.email_sent_message)
    #         else:
    #             messages.add_message(request, messages.SUCCESS, 'Please confirm your email address to complete the registration')
    #     return user




    # def verifyEmail_FBV(request, form, account_activition_email_template, mail_subject, showing_message_after_sending_email, email_sent_message):

    #     # save form in the memory not in database  
    #     user = form.save(commit=False)  
    #     user.is_active = False
    #     user.save()

    #     # to get the domain of the current site  
    #     current_site = get_current_site(request)  
    #     # mail_subject = 'Activation link has been sent to your email id' 
    #     message = render_to_string(account_activition_email_template, { 
    #         'user': user,  
    #         'domain': current_site.domain,
    #         'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
    #         'token':account_activation_token.make_token(user),  
    #     })
    #     to_email = form.cleaned_data.get('email')  
    #     email = EmailMessage(
    #                 mail_subject, message, to=[to_email]  
    #     )  
    #     email.send()

    #     if showing_message_after_sending_email:
    #         if isinstance(email_sent_message, str) or isinstance(email_sent_message, int):
    #             messages.add_message(request, messages.SUCCESS, email_sent_message)
    #         else:
    #             messages.add_message(request, messages.SUCCESS, 'Please confirm your email address to complete the registration')

    #     return user




class ActivateView(View):
    activitation_success_message = 'Thank you for your email confirmation. Now you can login your account.'
    activitation_fail_message = 'Activation link is invalid!'
    redirecting_after_activating = False
    """
    False: 
        returns HttpResponse after using link.
        set 'activitation_success_message' and 'activitation_fail_message' for changing default messages.
    True:
        redirects after using link.
        set 'activitation_success_redirecting_adderess' and 'activitation_fail_redirecting_adderess' for changing default redirecting adderesses.
    """
    activitation_success_template_address = None
    """
    Use it for setting address of activitation_success_template. By default, it's None.
    user objects data can be accessed by using 'user' in template.
    """
    activitation_fail_template_address = None
    """
    Use it for setting address of activitation_fail_template. By default, it's None.
    user objects data can be accessed by using 'user' in template.
    """



    def get(self, request, uidb64, token):  
        User = get_user_model() 
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)  
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None  
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True  
            user.save()

            if self.redirecting_after_activating == False:
                if isinstance(self.activitation_success_message, str) or isinstance(self.activitation_success_message, int):
                    return HttpResponse(self.activitation_success_message)
                else:
                    raise TypeError('Invalid input for \'activitation_success_message\'')
            else:
                context = { 'user' : user }
                return render(request, self.activitation_success_template_address, context=context)


        else:
            # if account_activation_token.check_token(user, token) == False:
            #         # to get the domain of the current site  
            #         current_site = get_current_site(request)  
            #         # mail_subject = 'Activation link has been sent to your email id' 
            #         message = render_to_string('acc_active_email.html', { 
            #             'user': user,  
            #             'domain': current_site.domain,
            #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
            #             'token':account_activation_token.make_token(user),  
            #         })
            #         to_email = user.email
            #         email = EmailMessage(
            #                     mail_subject, message, to=[to_email]  
            #         )  
            #         email.send()

            if self.redirecting_after_activating == False:
                if isinstance(self.activitation_fail_message, str) or isinstance(self.activitation_fail_message, int):
                    return HttpResponse(self.activitation_fail_message)
                else:
                    raise TypeError('Invalid input for \'activitation_fail_message\'')
            else:
                context = { 'user' : user }
                return render(request, self.activitation_fail_template_address, context=context)







class ActivateNewEmailView(View):
    activitation_success_message = 'Thank you for your email confirmation. Now you can login your account.'
    activitation_fail_message = 'Activation link is invalid!'
    redirecting_after_activating = False
    """
    False: 
        returns HttpResponse after using link.
        set 'activitation_success_message' and 'activitation_fail_message' for changing default messages.
    True:
        redirects after using link.
        set 'activitation_success_redirecting_adderess' and 'activitation_fail_redirecting_adderess' for changing default redirecting adderesses.
    """
    activitation_success_template_address = None
    """
    Use it for setting address of activitation_success_template. By default, it's None.
    user objects data can be accessed by using 'user' in template.
    """
    activitation_fail_template_address = None
    """
    Use it for setting address of activitation_fail_template. By default, it's None.
    user objects data can be accessed by using 'user' in template.
    """



    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token) and user.new_email is not None:
            user.email = user.new_email
            user.new_email = None 
            user.save()

            if self.redirecting_after_activating == False:
                if isinstance(self.activitation_success_message, str) or isinstance(self.activitation_success_message, int):
                    return HttpResponse(self.activitation_success_message)
                else:
                    raise TypeError('Invalid input for \'activitation_success_message\'')
            else:
                context = { 'user' : user }
                return render(request, self.activitation_success_template_address, context=context)


        else:
            if self.redirecting_after_activating == False:
                if isinstance(self.activitation_fail_message, str) or isinstance(self.activitation_fail_message, int):
                    return HttpResponse(self.activitation_fail_message)
                else:
                    raise TypeError('Invalid input for \'activitation_fail_message\'')
            else:
                context = { 'user' : user }
                return render(request, self.activitation_fail_template_address, context=context)
