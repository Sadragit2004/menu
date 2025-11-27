from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from ...forms.auth.verify_form import VerificationCodeForm
from ...model.user import CustomUser
from ...service.auth_service import AuthService

def verify_code(request):
    mobile = request.session.get("mobileNumber")
    next_url = request.session.get("next_url")
    if not mobile:
        messages.error(request, "شماره موبایل یافت نشد.")
        return redirect("account:send_mobile")

    user = CustomUser.objects.get(mobileNumber=mobile)
    security = AuthService.get_or_create_security(user)

    if request.method == "POST":
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['activeCode']
            try:
                AuthService.verify_code(security, code)
                AuthService.activate_user(user)
                login(request, user)
                messages.success(request, "✅ ورود با موفقیت انجام شد.")
                return redirect(next_url or "main:index")
            except Exception as e:
                messages.error(request, str(e))
                return redirect("account:verify_code")
    else:
        form = VerificationCodeForm()

    return render(request, "user_app/code.html", {"form": form, "mobile": mobile})
