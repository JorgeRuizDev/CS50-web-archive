from django import forms
from . import util

class NewSearchForm(forms.Form):
    searchField = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control mr-sm-2", "type": "search", "placeholder": "Entry Name",
               "aria-label": "Entry Name"}))


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            "type": "text",
            "class": "form-control",
            "placeholder": "Entry Name"
        }))



    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "type": "text",
            "class": "form-control rounded-0",
            "rows": "10",
            "placeholder": "Did you ever hear the tragedy of Darth Plagueis The Wise? "

                           "I thought not. It's not a story the Jedi would tell you. It's a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life… He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. "
                           "The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful… the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. Ironic. He could save others from death, but not himself."
            ,
        }
    ))

    def clean_title(self):
        title_var = self.cleaned_data.get("title")
        if util.entry_exists_case_insens(title_var):
            self.fields["title"].widget.attrs.update({"class": "form-control is-invalid"})
            print("No válido")
            raise forms.ValidationError("The entry already exists")
        else:
            return title_var

