from django import forms
from schemes.models import  Student_schemes





class Student_schemesform(forms.ModelForm):
    uniform_1 =forms.BooleanField()
    uniform_2 =forms.BooleanField()
    # uniform_3 =forms.BooleanField(initial=True)
    # uniform_4 =forms.BooleanField(initial=True)
    # textbook =forms.BooleanField(initial=True)
    # textbook_1 =forms.BooleanField(initial=True)
    # textbook_2 =forms.BooleanField(initial=True)
    # textbook_3 =forms.BooleanField(initial=True)
    # notebook =forms.BooleanField(initial=True)
    # notebook_1 =forms.BooleanField(initial=True)
    # notebook_2 =forms.BooleanField(initial=True)
    # notebook_3 =forms.BooleanField(initial=True)
    # bag =forms.BooleanField(initial=True)
    # footware =forms.BooleanField(initial=True)
    # sweater =forms.BooleanField(initial=True)
    # crayon =forms.BooleanField(initial=True)
    # colorpencil =forms.BooleanField(initial=True)
    # jeomatrybox =forms.BooleanField(initial=True)
    # atlas =forms.BooleanField(initial=True)
    # cycle =forms.BooleanField(initial=True)
    # laptop =forms.BooleanField(initial=True)
    # bw =forms.BooleanField(initial=True)
    # sci =forms.BooleanField(initial=True)

    class Meta:
        model=Student_schemes
