from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Thread, Message, Category
from .forms import ThreadForm, MessageForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = '/'

class ThreadListView(ListView):
    model = Thread
    template_name = 'thread_list.html'
    context_object_name = 'threads'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.message_set.filter(parent=None).order_by('created_at')
        context['message_form'] = MessageForm()
        return context

class MessageCreateView(View):
    def post(self, request, pk):
        thread = get_object_or_404(Thread, pk=pk)
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.author = request.user
            message.save()
            return redirect('thread_detail', pk=thread.pk)  

        messages = Message.objects.filter(thread=thread)  
        return render(request, 'thread_detail.html', {
            'thread': thread,
            'messages': messages,
            'message_form': form,
        })

@method_decorator(login_required, name='dispatch')
class ThreadCreateView(CreateView):
    model = Thread
    form_class = ThreadForm
    template_name = 'thread_form.html'
    success_url = reverse_lazy('thread_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def add_message(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.author = request.user
            parent_id = request.POST.get('parent_id')
            if parent_id:
                message.parent = get_object_or_404(Message, id=parent_id)
            message.save()
            return redirect('thread_detail', pk=thread_id)
    return redirect('thread_detail', pk=thread_id)

@login_required
def like_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if thread.likes.filter(id=request.user.id).exists():
        thread.likes.remove(request.user)
    else:
        thread.likes.add(request.user)
    return JsonResponse({'likes': thread.total_likes()})

@login_required
def like_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.likes.filter(id=request.user.id).exists():
        message.likes.remove(request.user)
    else:
        message.likes.add(request.user)
    return JsonResponse({'likes': message.total_likes()})

class ThreadSearchView(ListView):
    model = Thread
    template_name = 'thread_search.html'
    context_object_name = 'threads'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Thread.objects.filter(title__icontains=query)
        return Thread.objects.all()

def edit_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    if request.method == "POST":
        thread.title = request.POST.get('title')
        thread.content = request.POST.get('content')
        thread.save()
        return redirect('thread_detail', thread_id=thread.id)
    return render(request, 'edit_thread.html', {'thread': thread})

@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            return redirect('thread_list')
    else:
        form = ThreadForm()
    
    categories = Category.objects.all()
    return render(request, 'create_thread.html', {'form': form, 'categories': categories})
