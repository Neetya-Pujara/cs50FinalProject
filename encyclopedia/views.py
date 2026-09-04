from django import forms
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import choice
import markdown2

from . import util

def index(request):
    if request.method == "POST":
        query = request.POST['q'].lower()
        if (util.get_entry(query) != None):
            return HttpResponseRedirect(reverse("encyclopedia:topic", kwargs={"title":query}))
        entries=util.list_entries()
        newentries=[]
        l = len(query)
        for e in entries:
            entry=e.lower()
            curr=0
            works=False
            i=-1
            while i < len(entry)-1:
                i+=1
                if entry[i] != query[curr]:
                    if curr > 0:
                        i-=curr
                        curr=0
                    continue
                curr+=1
                if curr==l:
                    works=True
                    break
            if works:
                newentries.append(e)
        return render(request, "encyclopedia/index.html", {
                "entries": newentries
            })
                

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def topic(request, title):
    markdown_content = util.get_entry(title)
    if markdown_content == None:
        return render(request, "encyclopedia/topic.html", {
            "content" : None,
            "title" : title
        })
    converter = markdown2.Markdown()
    html_content = converter.convert(markdown_content)
    return render(request, "encyclopedia/topic.html", {
            "content" : html_content,
            "title" : title
        })

def new_page(request) :
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        if (util.get_entry(title) != None and request.POST['check'] == "newpage"):
            return render(request, "encyclopedia/error.html")
        util.save_entry(title,content)
        return HttpResponseRedirect(reverse("encyclopedia:topic", kwargs={"title":title}))
    else:
        return render(request, "encyclopedia/add.html", {
            "precontent" : "",
            "haveTitle" : None 
        })

def edit_page(request, title) :
    return render(request, "encyclopedia/add.html", {
        "precontent" : util.get_entry(title),
        "haveTitle" : title
    })

def random(request) :
    random_topic = choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:topic", kwargs={"title":random_topic}))