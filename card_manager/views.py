import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from card_manager.models import *
from card_manager.forms import *
from card_manager.utils import check_and_change_card_statuses

log = logging.getLogger(__name__)


@login_required
def cards_find_by(request):

    context = dict()

    context["cards_conditions_form"] = CardsConditionsForm()

    if request.POST and request.POST['action'] == "find_cards":
        form = CardsConditionsForm(request.POST)
        if form.is_valid():
            context["cards"] = form.get_cards()
        else:
            log.error(form.errors.as_data())
    else:
        context["cards"] = Card.objects.order_by('series').all()

    return render(request, "cards_find_by.html", context)


@login_required
def cards_generate(request):
    context = dict()

    return render(request, "cards_generate.html", context)


@login_required
def cards_card_edit(request, series, number):
    context = dict()

    card = Card.objects.filter(series=series).get(number=number)

    context["cards_conditions_form"] = CardEditForm()



    return render(request, "cards_edit_card.html", context)


@login_required
def cards_card_delete(request, card_series, card_id):
    context = dict()

    return render(request, "cards_card_delete.html", context)


