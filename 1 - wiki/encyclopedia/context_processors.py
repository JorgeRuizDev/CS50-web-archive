from . import views

def add_variable_to_context(request):
    return {
        'search_form': views.NewSearchForm()
    }

