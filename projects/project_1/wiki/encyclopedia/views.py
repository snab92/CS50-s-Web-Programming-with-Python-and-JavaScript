from django.shortcuts import render
from django.http import HttpResponse
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)

    if entry_content is None:
        return HttpResponse("Entry does not exist")
    
    #convert markdown to HTML
    html_content = markdown.markdown(entry_content)
    
    return render(request, "encyclopedia/entries.html", {
        "title": title,
        "content": html_content
    })
    
