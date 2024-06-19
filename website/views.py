from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User


from .encryption import Encryption
from . import models
from . import forms
# Create your views here.


class MainView(TemplateView):
    template_name = 'website/index.html'


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'website/profile.html'


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.UserForm
    template_name = 'website/profile.html'

    def get_success_url(self) -> str:
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.kwargs.get('pk'):
            messages.error(request, 'You can\'t edit other users profile')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
    



class VaultView(LoginRequiredMixin, ListView):
    model = models.Credential
    template_name = 'website/password_vault.html'

    def get_queryset(self):
        return models.Credential.objects.filter(user=self.request.user)

    def get(self, request: HttpRequest):
        if request.session.get('show_second_modal', None):
            encryption = Encryption()
            cred_pk = request.session['cred_pk']
            context = self.get_context_data(
                object_list=models.Credential.objects.filter(user=self.request.user))
            context['credential_password'] = encryption.decrypt_data(self.model.objects.filter(
                user=self.request.user).get(pk=cred_pk).credential_password)
            context['show_second_modal'] = True
            request.session.pop('show_second_modal', None)
            request.session.pop('cred_pk', None)
            return render(request, self.template_name, context)
        return super().get(request)

    def post(self, request):
        password = request.POST.get('password')

        check = request.user.check_password(password)
        if not check:
            messages.error(request, 'Incorrect password!',
                           extra_tags='vault_error')
        else:
            cred_pk = request.POST.get('credential_pk')

            # Create session variables to handle successful POST without rendering template with context, that way we avoid form resubmission
            request.session['show_second_modal'] = True
            request.session['cred_pk'] = cred_pk
        return redirect('vault')
        # return render(request, self.template_name, {'credential_list': self.model.objects.all(), 'check': check, 'credential_password': credential_password})

    @method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True))
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template_name, {'form': self.form_class})


class MyLoginView(LoginView):
    def get(self, request):
        form = self.form_class
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.template_name, {'form': form})


class AddCredentialView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('add')
    form_class = forms.AddCredentialForm
    template_name = 'website/add_credential.html'

    def form_valid(self, form):
        credential = form.save(commit=False)
        credential.user = self.request.user

        encryption = Encryption()

        credential.credential_password = encryption.encrypt_data(
            credential.credential_password)
        credential.save()
        messages.success(
            self.request, 'Credential was added successfully.', extra_tags='added_credential')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, 'The form was not submitted successfully.', extra_tags='failed_add_credential')
        return super().form_valid(form)


@login_required
def edit_credential(request, pk):
    credential = get_object_or_404(models.Credential, pk=pk)
    encryption = Encryption()
    if request.method == 'POST':
        form = forms.AddCredentialForm(request.POST, instance=credential)
        if form.is_valid():
            credential.credential_password = encryption.encrypt_data(
                credential.credential_password)
            credential.save()
            form.save()
        else:
            messages.error(
                request, 'The form was not submitted successfully.', extra_tags='vault_error')
        return redirect('vault')
    else:
        form = forms.AddCredentialForm(instance=credential)
        form.data['credential_password'] = ''
        return render(request, 'website/password_vault.html', {'form': form, 'edit_pk': pk, 'credential_list': models.Credential.objects.filter(user=request.user)})


class DeleteCredentialView(LoginRequiredMixin, DeleteView):
    model = models.Credential
    success_url = reverse_lazy('vault')
