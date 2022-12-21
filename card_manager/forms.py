# -*- coding: utf-8 -*-
import logging
import random
import sys
from datetime import datetime, timedelta

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


class GenerateCardsForm(forms.Form):
    series = forms.IntegerField(min_value=1)
    amount = forms.IntegerField(min_value=1)
    expiration_date = forms.ChoiceField(choices=[(timedelta(days=int(365)), '1 year'),
                                                 (timedelta(days=int(182)), '6 month'),
                                                 (timedelta(days=int(30)), '1 month'), ])

    status = forms.ChoiceField(choices=[('Not activated', 'Not activated'),
                                        ('Activated', 'Activated'), ])

    def generate(self):
        cleaned_data = self.cleaned_data
        series = cleaned_data.get('series')
        for i in range(1, cleaned_data.get('amount')):
            while True:
                number = random.randint(1, sys.maxsize)
                if not Card.objects.filter(series=series).filter(number=number).exists():
                    break

            card = Card(series=series,
                        number=number,
                        release_date=datetime.now(),
                        end_date=datetime.now() + timedelta(days=int(cleaned_data.get('expiration_date').split()[0])),
                        status=cleaned_data.get('status'))
            card.save()


class CardEditForm(forms.ModelForm):
    id = forms.IntegerField()
    status = forms.ChoiceField(choices=Card.STATUS_CHOICES)

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        card = Card.objects.get(id=cleaned_data.get('id'))
        card.status = cleaned_data.get('status')

        if commit:
            card.save()

    class Meta:
        model = Card
        exclude = ('series', 'number', 'release_date', 'end_date', 'status')


class CardDeleteForm(forms.Form):

    def delete(self, series, number):
        card = Card.objects.filter(series=series).get(number=number)
        card.delete()


class UpdateStatusesForm(forms.Form):

    def update(self):
        cards = Card.objects.filter(status='Activated').filter(end_date__lte=datetime.now())
        for card in cards:
            card.status = 'Expired'
            card.save()
