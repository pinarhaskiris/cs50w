from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from random import randint
from markdown2 import Markdown

from . import util
	
entries = util.list_entries()

class newEntryForm(forms.Form):
	#will be used when creating a new page
	entryName = forms.CharField(label='Entry Name', 
                    widget=forms.TextInput(attrs={'placeholder': 'Write your title here...'}))
	content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":5, 'placeholder': 'Write your content in Markdown format here...'}), label="")

class editForm(forms.Form):
	#will be used when editing a page
	entryName = forms.CharField(widget=forms.TextInput())
	content = forms.CharField(widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def goToEntry(request, entryName):
	content = util.get_entry(entryName)
	markdowner = Markdown()

	if content == None:
		return render(request, "encyclopedia/error.html")
	else:
		return render(request, "encyclopedia/entryName.html", {
			"entryContent": markdowner.convert(content),
			"entryName": entryName
			})

def search(request):
	posted = request.POST
	item = posted["item"]
	markdowner = Markdown()

	for entry in entries:
		if entry.lower() == item.lower():
			return render(request, "encyclopedia/entryName.html", {
				"entryContent": markdowner.convert(util.get_entry(entry)),
				"entryName": item
				})
	
	return render(request, "encyclopedia/failedSearch.html", {
       	"entries": util.list_entries(),
       	"item": item
    })

def createNewPage(request):
	if request.method == "POST":
		form = newEntryForm(request.POST)
		if form.is_valid():

			#extracting necessary variables such as the name and the content of the new entry
			newEntry = form.cleaned_data["entryName"]
			entryContent = form.cleaned_data["content"]

			#checking if the entry already exists
			for entry in entries:
				if newEntry == entry:
					return render(request, "encyclopedia/entryAlreadyExists.html")

			entryFile = open(f"entries/{newEntry}.md", "w+")

			entries.append(newEntry)
			entryFile.write(entryContent)

			entryFile.close()

			return HttpResponseRedirect(f"wiki/{newEntry}")
		else:
			return render(request, "encyclopedia/createNewPage.html",  {
				"form": form
				})

	return render(request, "encyclopedia/createNewPage.html", {
		"form": newEntryForm()
		})

def randomPage(request):
	markdowner = Markdown()
	randomNumber = randint(0, len(entries)-1)
	return render(request, "encyclopedia/entryName.html", {
				"entryContent": markdowner.convert(util.get_entry(entries[randomNumber])),
				"entryName": entries[randomNumber]
				})

def editPage(request, entryName):
	existingContent = util.get_entry(entryName)

	initial = {'entryName': entryName, 'content': existingContent}

	if request.method == "POST":
		#creating a form with the initial content
		form = editForm(request.POST, initial=initial)
		if form.is_valid():
			#extracting the user inputs
			updatedEntryName = form.cleaned_data["entryName"]
			updatedContent = form.cleaned_data["content"]

			#updating the entry content
			entryFile = open(f"entries/{entryName}.md", "w+")
			entryFile.write(updatedContent)
			entryFile.close()

			return HttpResponseRedirect(f"/wiki/{entryName}")
		else:

			return render(request, "encyclopedia/editPage.html",  {
				"entryName": entryName,
				"form": form
				})

	return render(request, "encyclopedia/editPage.html", {
		"entryName": entryName,
		"form": editForm(initial=initial)
		})

	






