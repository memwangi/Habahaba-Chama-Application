from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from .models import Member, Chama, Transaction
from .forms import RegisterForm, CreateChamaForm, TransactionForm, AddMemberForm
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


@login_required
def homepage(request):
    return render(request, 'chama/home_view.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'chama/register.html', {'form': form})

# Create,update and list chamas, you can also access chama details


class ChamaListView(ListView):
    model = Chama


class ChamaDetailView(DetailView):
    model = Chama


class ChamaCreate(CreateView):
    model = Chama
    form_class = CreateChamaForm
    success_url = reverse_lazy('ch')

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        return super().form_valid(form)

    def make_admin_member(self):
        self.members_set.add(self.request.user)
        self.save()


class ChamaUpdate(UpdateView):
    model = Chama
    fields = ['groupName', 'paybillNo',
              'contribution_amnt', 'contribution_interval']


class CurrentUserChamas(ListView):
    model = Chama
    template_name = 'chama/chama_list_current_user.html'
    paginate_by = 10

    def get_queryset(self):
        return Chama.objects.filter(created_by=self.request.user) | Chama.objects.filter(members__phone_number=self.request.user.phone_number)

# End chama models


class TransactionCreate(CreateView):
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Add other fields required before saving the transaction"""
        chama = get_object_or_404(Chama, pk=self.kwargs['pk'])
        phone = self.request.user.phone_number
        form.instance.chama = chama
        form.instance.transaction_time = timezone.now()
        form.instance.phone_number = phone
        form.instance.member = self.request.user
        return super().form_valid(form)


class TransactionDetailView(DetailView):
    pass


class TransactionListView(ListView):
    pass

@login_required
def ChamaAddMember(request, pk):
    """Add member to a chama"""
    chama = get_object_or_404(Chama, id=pk)
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        if form.is_valid():
            phonenumber = form.cleaned_data['phone']
            member = Member.objects.get(phone_number=phonenumber)
            chama.members_set.add(member)
            url = chama.get_absolute_url()
            return redirect(url)

    else:
        form = AddMemberForm()
    return render(request, 'chama/add_member.html', {'form': form, 'key': pk})
