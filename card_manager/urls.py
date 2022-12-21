from django.urls import path

from card_manager.views import cards_find_by, cards_card_edit, cards_card_delete, cards_generate


urlpatterns = [
    path('cards/find_by/', cards_find_by, name="cards_find_by"),

    path('cards/generate/', cards_generate, name="cards_generate"),

    path('cards/card/edit/series=<int:series>?number=<int:number>',
         cards_card_edit, name="cards_card_edit"),

    path('cards/delete/series=<int:series>?number=<int:number>',
         cards_card_delete, name="cards_card_delete"),
]
