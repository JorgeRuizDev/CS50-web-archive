from django.shortcuts import render
from django.shortcuts import redirect

from .forms import NewEntryForm
from .forms import NewSearchForm

from . import util

from random import choice

import markdown2


def index(request):
    """
     request: is a HTTP request
     This returns an HTTP response for the following url:
     index is in the urls.py
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": NewSearchForm()
    })


def render_wiki(request, wiki_name):
    """
    request: request object
    wiki_name: The name of the entry to be rendered
    """
    if not util.entry_exists(wiki_name):
        return error_reply(request, wiki_name)

    context = {
        "wiki_title": wiki_name,
        "wiki_body": markdown2.markdown(util.get_entry(wiki_name))
    }

    return render(request, "encyclopedia/wiki_layout.html", context)


def search(request):
    """
    search view:
    -Renders a wiki if the request string matches (case sensitive) with an entry filename
    -If there isn't a matching file, it returns a list with matching substrings.
    -If the post request is not valid, it renders the index
    request: Http request with the POST form with a "searchField" name.
    """
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search_string = form.cleaned_data["searchField"]

            if util.entry_exists(search_string):
                return render_wiki(request, search_string)
            else:
                return view_similar_results(request, search_string)
    else:
        return render(request, "encyclopedia/index.html")

def view_similar_results(request, search_string):
    """
    renders a list with substring matching filenames of the search_string.
    request: Request object.
    search_string: the search string.
    """
    similar_entries = util.similar_results(search_string)

    return render(request, "encyclopedia/search_results.html", {
        "entry_size": len(similar_entries),
        "is_one_result": bool(len(similar_entries) == 1),
        "entries": similar_entries
    })


def error_reply(request, wiki_name):
    """
    Renders a 404 page with a custom message.
    wiki_name: String of the missing entry.
    """
    return render(request, "encyclopedia/entry_not_found.html", {
        "wiki_title": f"{wiki_name} not found",
        "entry_name": wiki_name
    }
                  )


def view_error404(request, exception):
    """
    Default 404 page for production
    exception: 404 exception, not used, but needed to be used as the default 404 page
    """
    print(exception)
    return error_reply(request, "404")


def edit_entry(request):
    """
    View that edits an entry.
    It uses the same template as add_entry()
    """
    entry = request.GET.get("entry")

    if not util.entry_exists(entry):
        return error_reply(request, entry)

    body = "\n".join(util.get_entry(entry).split("\n")[2:])
    form = NewEntryForm(initial={'body': body})

    if request.POST.get("done") == "True":
        util.save_entry(entry, request.POST.get("body"))
        return render_wiki(request, entry)

    context = {
        "form": form,
        "is_edit_page": True,
        "title_edit": entry
    }

    if request.POST.get("preview") == "True":
        body = markdown2.markdown(request.POST['body'])

        context["preview"] = True
        context["md_title"] = entry
        context["md_content_as_HTML"] = body
        context["form"] = NewEntryForm(initial={'body': request.POST.get("body")})

    return render(request, "encyclopedia/new_page.html", context)


def add_entry(request):
    """
    View to add a new entry.
    """
    form = NewEntryForm(request.POST or None)

    context = {
        "form": form,
    }

    if request.POST.get("title") is None:
        return render(request, "encyclopedia/new_page.html", {
            "form": form
        })
    if form.is_valid() and request.POST.get("done") == "True":
        util.save_entry(request.POST.get("title"), request.POST.get("body"))
        return render_wiki(request, request.POST.get("title"))

    if form.is_valid() and request.POST.get("preview") == "True":
        context["preview"] = True
        context["md_title"] = form.cleaned_data["title"]
        context["md_content_as_HTML"] = markdown2.markdown(form.cleaned_data['body'])

    if not form.is_valid():
        context["feedback"] = True

    return render(request, "encyclopedia/new_page.html", context)


def view_random_entry(request):
    """
    View for /random
    render a random entry.
    """
    return redirect(f"wiki/{choice(util.list_entries())}")
