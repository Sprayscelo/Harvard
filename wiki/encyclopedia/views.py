from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
import markdown2
from . import util
from django import forms
from django.contrib import messages
import random

class NewEntryForm(forms.Form):
    tittle = forms.CharField(label="Tittle")
    textarea = forms.CharField(label="Content (Markdown)", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, linguage):
    content = util.get_entry(linguage)
    converted = markdown2.markdown(content)
    
    return render(request, "encyclopedia/content.html", {
        "page": converted,
        "entry": linguage
    })

def search(request):
    for i in util.list_entries():
        if request.method == "POST" and request.POST["searched"] == i:
            searched = request.POST["searched"]
            return HttpResponseRedirect(f"/wiki/{searched}")
    return render(request, "encyclopedia/search.html", {
        "searched": request.POST["searched"],
        "entry":util.list_entries
    })

def newpage(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            valid_tittle = form.cleaned_data["tittle"]
            valid_textarea = form.cleaned_data["textarea"]
            allentries = list(map(lambda x : x.casefold(), util.list_entries()))
            if valid_tittle.casefold() not in allentries:
                util.list_entries().append(util.save_entry(valid_tittle, valid_textarea))
                return HttpResponseRedirect(f"/wiki/{valid_tittle}")
            else: messages.error(request, "This tittle already exists") 
            return redirect("/wiki/newpage/")
    return render(request, "encyclopedia/newpage.html", {
        "forms": NewEntryForm()
    })

def edit(request, entry):
    class NewEditForm(forms.Form):
        editedtittle = forms.CharField(label="Tittle", initial=entry, disabled=True)
        editedtextarea = forms.CharField(label="Content (Markdown)", widget=forms.Textarea, initial=util.get_entry(entry))
    if request.method == "POST":
        form = NewEditForm(request.POST)
        if form.is_valid():
            valid_editedtittle = form.cleaned_data["editedtittle"]
            valid_editedtextarea = form.cleaned_data["editedtextarea"]
            util.save_entry(valid_editedtittle, valid_editedtextarea)
            return HttpResponseRedirect(f"/wiki/{entry}")
    return render(request, "encyclopedia/edit.html", {
        "lin": entry,
        "content": util.get_entry(entry),
        "form": NewEditForm()
    })

def ran(request):
    routelist = util.list_entries()
    randomroute = random.choice(routelist)
    return HttpResponseRedirect(f"/wiki/{randomroute}")