import logging
from django.contrib import admin
from django import forms

from card_manager.models import Card, Purchase

log = logging.getLogger(__name__)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('get_purchase_id', 'sum', 'get_purchase_series_and_number')

    @admin.display(ordering='questionnaire__title', description='Questionnaire')
    def get_purchase_series_and_number(self, purchases):
        return f"{purchases.card.series}-{purchases.card.number}"

    @admin.display(ordering='questionnaire__title', description='Questionnaire')
    def get_purchase_id(self, purchases):
        return f"Purchase object({purchases.id})"


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('get_card_id', 'series', 'release_date', 'end_date', 'status', 'get_purchases')

    @admin.display(description='Purchases')
    def get_purchases(self, card):
        purchases = list(map(lambda x: "Purchase object(" + str(x.id) + "): " + str(x.sum) + " \n",
                             Purchase.objects.filter(card=card).order_by('card')))
        return purchases

    @admin.display(ordering='questionnaire__title', description='Questionnaire')
    def get_card_id(self, card):
        return f"Card object({card.number})"
