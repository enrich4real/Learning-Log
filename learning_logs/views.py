from django.shortcuts import render, redirect
from.forms import TopicForm, EntryForm

from .models import Topic, Entry


# Create your views here.

def index(request):
    """The Home page for learning log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render (request,'learning_logs/topics.html',context)

def topic(request, topic_id):
    """show a single topic"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render (request,'learning_logs/topic.html',context)

def new_topic(request):
    #adds a new topic
    if request.method != 'POST':
        #no data submitted, create a blank form
        form = TopicForm()
    else:
        #POST data submitted, process the data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
        
    #Display a blank or invalid form
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

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


def edit_entry(request, entry_id):
    #edit an existing entry
    entry  = Entry.objects.get(id=entry_id)
    topic = entry.topic

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