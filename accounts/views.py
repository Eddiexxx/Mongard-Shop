from django.shortcuts import render , redirect
from django.contrib import messages
from django.views import View
from .forms import UserRegistrationForm, VerifyCodeForm
from random import randint
from utils import send_otp_code
from .models import OtpCode, User
from datetime import timedelta
from django.utils import timezone
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name,{'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
            }
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})






class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    def get(self,request):
        form = self.form_class
        return render(request,'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            # Calculate two minutes later from the `created` field
            two_minutes_later = code_instance.created + timedelta(minutes=2)
            current_time = timezone.now()  # Get the current time

            # Check both conditions: not past two minutes and the code matches
            if current_time <= two_minutes_later and cd['code'] == code_instance.code:
                # Create the user if both conditions are true
                User.objects.create_user(
                    user_session['phone_number'],
                    user_session['email'],
                    user_session['full_name'],
                    user_session['password']
                )
                code_instance.delete()
                messages.success(request, 'You are registered!', 'success')
                return redirect('home:home')
            else:
                # Handle cases where the code is wrong or has expired
                if current_time > two_minutes_later:
                    messages.error(request, 'The code has expired.', 'danger')
                else:
                    messages.error(request, 'This code is wrong.', 'danger')
                return redirect('account:verify_code')

        return redirect('home:home')




# if form.is_valid():
        #     cd=form.cleaned_data
        #     two_minutes_later= code_instance.created + timedelta(minutes=2)
        #     current_time = timezone.now()
        #     if current_time <= two_minutes_later and cd['code'] == code_instance.code:
        #         User.objects.create_user(user_session['phone_number'], user_session['email'], user_session['full_name'], user_session['password'])
        #         code_instance.delete()
        #         messages.success(request, 'you registered', 'success')
        #         return redirect('home:home')
        #     else:
        #         messages.error(request, 'this code is wrong', 'danger')
        #         return redirect('account:verify_code')
        #
        # return redirect('home:home')