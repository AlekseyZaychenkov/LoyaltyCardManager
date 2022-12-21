from django.urls import path

from card_manager.views import cards_find_by, cards_card_edit, cards_card_delete, cards_generate


urlpatterns = [

    path('cards/find_by/', cards_find_by, name="cards_find_by"),

    # path('cards/find_by'
    #      '/series_from=<int:series_from>?series_to=<int:series_to>'
    #      '?number_from=<int:number_from>?number_to=<int:number_to>'
    #      '?release_date_from=<str:release_date_from>?release_date_to=<str:release_date_to>'
    #      '?end_date_from=<str:end_date_from>?end_date_to=<str:end_date_to>'
    #      '?status=<str:status>/', cards_find_by, name="cards_find_by"),

    # path('cards/all/', cards_find_by, name="cards_all"),
    # path('cards/find_by/series/', cards_find_by, name="cards_find_by_series"),
    # path('cards/find_by/number/', cards_find_by, name="cards_find_by_number"),
    # path('cards/find_by/release_date/', cards_find_by, name="cards_find_by_release_date"),
    # path('cards/find_by/end_date/', cards_find_by, name="cards_find_by_end_date"),
    # path('cards/find_by/status/', cards_find_by, name="cards_find_by_status"),
    path('cards/generate/', cards_generate, name="cards_generate"),
    path('cards/series=<int:series>?number=<int:number>/edit/',
         cards_card_edit, name="cards_edit_card"),
    path('cards/series=<int:series>?number=<int:number>/delete/',
         cards_card_delete, name="cards_card_delete"),
]
