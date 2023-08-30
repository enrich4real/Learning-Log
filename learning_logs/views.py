from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.forms import TopicForm, EntryForm
from django.http import Http404

from .models import Topic, Entry


# Create your views here.

def index(request):
    """The Home page for learning log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    #show all topics
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render (request,'learning_logs/topics.html',context)

@login_required
def topic(request, topic_id):
    """show a single topic"""
    topic = Topic.objects.get(id=topic_id)
    #make sure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render (request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    #adds a new topic
    if request.method != 'POST':
        #no data submitted, create a blank form
        form = TopicForm()
    else:
        #POST data submitted, process the data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            return redirect('learning_logs:topics')
        
    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    #adds a new entry for a given topic
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #no data submitted, create a blank form
        form = EntryForm()

    else:
        #POST data submitted, process the data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry= form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
        
    #Display a blank or invalid form
    context = {'topic':topic,'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    #edit an existing entry
    entry  = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #initial request
        form = EntryForm(instance=entry)
    else:
        #POST data submitted, process the data
        form = EntryForm( instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    
    context = {'entry':entry, 'topic':topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


