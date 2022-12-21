# -*- coding: utf-8 -*-
import logging

from django import forms
from django.core.validators import MinValueValidator

from card_manager.models import Card

log = logging.getLogger(__name__)


class CardsConditionsForm(forms.Form):
    series_from = forms.IntegerField(required=False, min_value=1)
    series_to = forms.IntegerField(required=False, min_value=1)
    number_from = forms.IntegerField(required=False, min_value=1)
    number_to = forms.IntegerField(required=False, min_value=1)
    status = forms.ChoiceField(choices=Card.STATUS_CHOICES)
    release_date_from = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=False)
    release_date_to = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=False)
    end_date_from = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=False)
    end_date_to = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=False)

    def get_cards(self):
        cards = Card.objects.all()
        cleaned_data = self.cleaned_data

        if cleaned_data.get("series_from"):
            cards = cards.filter(series__gte=cleaned_data.get("series_from"))
        if cleaned_data.get("series_to"):
            cards = cards.filter(series__lte=cleaned_data.get("series_to"))

        if cleaned_data.get("number_from"):
            cards = cards.filter(number__gte=cleaned_data.get("number_from"))
        if cleaned_data.get("number_to"):
            cards = cards.filter(number__lte=cleaned_data.get("number_to"))

        if cleaned_data.get("status"):
            cards = cards.filter(status=cleaned_data.get("status"))

        if cleaned_data.get("release_date_from"):
            cards = cards.filter(release_date__gte=cleaned_data.get("release_date_from"))
        if cleaned_data.get("release_date_to"):
            cards = cards.filter(release_date__lte=cleaned_data.get("release_date_to"))

        if cleaned_data.get("end_date_from"):
            cards = cards.filter(end_date__gte=cleaned_data.get("end_date_from"))
        if cleaned_data.get("end_date_to"):
            cards = cards.filter(end_date__lte=cleaned_data.get("end_date_to"))

        return cards


class CardEditForm(forms.ModelForm):
    number = forms.IntegerField()
    series = forms.IntegerField()
    release_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
    status = forms.ChoiceField(choices=Card.STATUS_CHOICES)

    def save(self, commit=True):
        card = self.instance
        if commit:
            card.save()

    class Meta:
        model = Card
        exclude = ('schedule',)

