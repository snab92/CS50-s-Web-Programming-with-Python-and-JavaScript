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
      
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),                     
        # Pass the form to the template
        "search_form": SearchForm()
    })

#use of the util function to get what is on the .md file 
def entry(request, title):
    title_lower = title.lower()

    for entry in util.list_entries():
        if title_lower == entry.lower():
            entry_content = util.get_entry(entry)
            break
        else:
            entry_content = None

# show error message
    if entry_content is None:
        return render(request, "encyclopedia/index.html", {
            "error_message": "The requested page was not found.", 
            "search_form": SearchForm()         
        })

    #convert markdown to HTML
    html_content = markdown.markdown(entry_content)
    
    # Add the form to the context
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": html_content,
        "search_form": SearchForm()
    })


def search(request):
    if request.method == "POST":
    # Create form instance with POST data
        form = SearchForm(request.POST)                    
        if form.is_valid(): 
            # Get validated search term
            query = form.cleaned_data['query']  
            query_lower = query.lower()

            # check if entry exists
            for entry in util.list_entries():
                if query_lower == entry.lower():
                    return redirect('entry', title = query)    

                else:                    
                    # Handle partial matches
                    matching_entries = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
                    return render(request, "encyclopedia/index.html", {
                        "entries": matching_entries,
                        "search_query": query,
                        "search_form": SearchForm()
                    })


    

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
                    "error_message": "An entry with this title already exists.",
                    "search_form": SearchForm()
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(f"/wiki/{title}")
    else:
        form = NewPage()
        
    return render(request, "encyclopedia/new_page.html",{
        "search_form": SearchForm(),
        "form": form
    })
