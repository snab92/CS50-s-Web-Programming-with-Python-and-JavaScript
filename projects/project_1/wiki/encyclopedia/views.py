from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django import forms
import markdown
import random

from . import util


class NewPage(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField( widget=forms.Textarea, label="Content")


def convertmd_tohtml(title):
    title_low = title.lower()
    for entry in util.list_entries():
        if title_low == entry.lower():
            content = util.get_entry(entry)
            break
    else:
        return None
    
    if content is not None:
        markdowner = markdown.Markdown()
        return markdowner.convert(content)
    else:
        return None


def index(request):    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),                     
    })


#use of the util function to get what is on the .md file 
def entry(request, title):
    html_content = convertmd_tohtml(title)
    if html_content == None:
        return render(request, "encyclopedia/index.html", {
            "error_message": "The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entries.html",{
            "title": title,
            "content": html_content,
        })

def search(request):
    if request.method == "POST":
    # Create form instance with POST data
        query = request.POST["q"]
        html_content = convertmd_tohtml(query)
        if html_content is not None:
            return render(request, "encyclopedia/entries.html",{
                "title": query,
                "content": html_content
            })
        else:
            all_entries = util.list_entries()
            matches = []
            for entry in all_entries:
                if query.lower() in entry.lower():
                    matches.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": matches                     
            })
    else:  # GET request
        return redirect('index')
    

def new_page(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            existing_entries = util.list_entries()
            if any(title.lower() == entry.lower() for entry in existing_entries):
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error_message": "An entry with this title already exists."
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
    else:     
        return render(request, "encyclopedia/new_page.html",{
            "form": NewPage()
        })


def edit(request):
    if request.method == "POST":  
        print(request.POST)  
        title = request.POST['entry_title']      
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })
    

def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]      
        content = request.POST["content"]  
        util.save_entry(title, content)     
        return HttpResponseRedirect(f"/wiki/{title}")
    

def random_entry(request):
    entries = util.list_entries()
    n = random.randint(0,(len(entries)-1))
    rand = entries[n]
    return HttpResponseRedirect(f"/wiki/{rand}")

