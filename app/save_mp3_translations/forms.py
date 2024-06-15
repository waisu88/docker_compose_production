from django import forms

lang_choices = [
    ("en", "English"),
    ("pl", "Polish"),
    ("hr", "Croatian"),
    ("fr", "French"),
    ("ru", "Russian"),
    ("es", "Spanish"),
    ("ko", "Korean"),
    ("zh-CN", "Chinese (simplified)")
]


class MP3FinnForm(forms.Form):
    words1 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count1 = forms.IntegerField(max_value=5, min_value=1)
    words2 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count2 = forms.IntegerField(max_value=5, min_value=1)
    words3 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count3 = forms.IntegerField(max_value=5, min_value=1)
    words4 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count4 = forms.IntegerField(max_value=5, min_value=1)
    words5 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count5 = forms.IntegerField(max_value=5, min_value=1)
    words6 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count6 = forms.IntegerField(max_value=5, min_value=1)
    words7 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count7 = forms.IntegerField(max_value=5, min_value=1)
    words8 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count8 = forms.IntegerField(max_value=5, min_value=1)
    words9 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count9 = forms.IntegerField(max_value=5, min_value=1)
    words10 = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=100, required=False)
    count10 = forms.IntegerField(max_value=5, min_value=1)

    enter_language = forms.ChoiceField(label='Choose enter language', choices=lang_choices, initial='en')
    destination_language = forms.ChoiceField(label='Choose destination language', choices=lang_choices, initial='pl')


class MP3Form(forms.Form):
    words = forms.CharField(label='Enter sentences or words. Remember to end every sentence/word with ".", "!" or "?"', max_length=3000)
    enter_language = forms.ChoiceField(label='Choose enter language', choices=lang_choices, initial='en')
    destination_language = forms.ChoiceField(label='Choose destination language', choices=lang_choices, initial='pl')
   