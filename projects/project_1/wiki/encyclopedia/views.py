from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from django import forms
import markdown


from . import util

class SearchForm(forms.Form):
    query = forms.CharField(label="Search")


class NewPage(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField( widget=forms.Textarea, label="Content")

    



def index(request):
    if request.method == "POST":
        # Create form instance with POST data
        form = SearchForm(request.POST)                     
        if form.is_valid(): 
            # Get validated search term
            query = form.cleaned_data['query']                
            # check if entry exists
            if query in util.list_entries():                         
                return redirect('entry', title = query)    
            else:
                # Handle partial matches
                matching_entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
                return render(request, "encyclopedia/index.html", {
                    "entries": matching_entries,
                    "search_query": query,
                    "search_form": SearchForm()
                })
    else:
        form = SearchForm()

    #use of the util function to display all the entries   
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),                     
        # Pass the form to the template
        "form": form
    })

    #use of the util function to get what is on the .md file 
def entry(request, title):
    entry_content = util.get_entry(title)                   

    # use of the Http 404
    if entry_content is None:
        return Http404("Entry does not exist")              
    
    #convert markdown to HTML
    html_content = markdown.markdown(entry_content)
    
    # Add the form to the context
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": html_content,
        "form": SearchForm()
    })
    

def new_page(request):
    if request.method == "post":
        form = NewPage(request.post)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return render(request, "encyclopedia/new_page.html", {
                    "form": form,
                    "error_message": "An entry with this title already exists."
                })
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
    else:
        form = NewPage()
        
    return render(request, "encyclopedia/new_page.html",{
        "search_form": SearchForm(),
        "form": form
    })
