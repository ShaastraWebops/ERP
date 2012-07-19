from django.db import models
from django.forms import ModelForm
from feedback.models import *
from django import forms

from django.utils.safestring import mark_safe

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

RATING_CHOICES= [(i,i) for i in range(11)]


class QuestionFormCoord (ModelForm):
    class Meta:
        model = Question
        fields= ('question','answered_by','departments',)


class QuestionFormCore (ModelForm):
    class Meta:
        model = Question
        fields= ('question','departments',)

class AnswerForm (ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES,widget=forms.RadioSelect)
    class Meta:
        model = Answer
        fields = ('rating',)



