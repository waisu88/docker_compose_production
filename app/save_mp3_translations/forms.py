from django import forms

lang_choices = [
    ("en", "English"),
    ("pl", "Polish"),
    ("hr", "Croatian"),
    ("fr", "French"),
    ("ru", "Russian"),
    ("es", "Spanish"),
]


class MP3Form(forms.Form):
    words = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=500)
    enter_language = forms.ChoiceField(label='Choose enter language', choices=lang_choices, initial='hr')
    destination_language = forms.ChoiceField(label='Choose destination language', choices=lang_choices, initial='pl')
