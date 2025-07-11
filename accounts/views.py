from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/profile.html', {'form': form})

# <form method="post">
#   {% csrf_token %}
#   <input type="text" name="username" placeholder="اسم المستخدم">
#   <input type="password" name="password" placeholder="كلمة المرور">
#   <button type="submit">دخول</button>
# </form>
# <a href="{% url 'social:begin' 'google-oauth2' %}?next=/accounts/profile/">تسجيل الدخول بـ Google</a><br>
# <a href="{% url 'social:begin' 'facebook' %}?next=/accounts/profile/">تسجيل الدخول بـ Facebook</a>

# # templates/accounts/register.html
# <form method="post">
#   {% csrf_token %}
#   {{ form.as_p }}
#   <button type="submit">تسجيل</button>
# </form>

# # templates/accounts/profile.html
# <form method="post" enctype="multipart/form-data">
#   {% csrf_token %}
#   {{ form.as_p }}
#   <button type="submit">حفظ</button>
# </form>
# <a href="{% url 'logout' %}">تسجيل الخروج</a>
# <a href="https://mail.google.com" target="_blank" class="btn btn-primary">
#     افتح بريدك الإلكتروني
# </a>
# <a href="mailto:" class="btn btn-secondary">
#     افتح البريد الافتراضي
# </a>
# <p>تم إنشاء حسابك بنجاح ✅</p>
# <p>راجع بريدك الإلكتروني لتفعيل الحساب أو متابعة طلباتك.</p>
# <a href="https://mail.google.com" target="_blank">اضغط هنا لفتح Gmail</a>
# <h3>مرحبًا {{ user.username }} 👋</h3>
# <p>راجع بريدك (<strong>{{ user.email }}</strong>) لتأكيد حسابك أو التواصل معنا.</p>
# <a href="https://mail.google.com/mail/u/0/#inbox" target="_blank" class="btn btn-success">افتح Gmail الآن</a>
