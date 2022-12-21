from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from card_manager.models import *
from card_manager.forms import *

log = logging.getLogger(__name__)



@login_required
def cards_find_by(request):
    context = dict()
    context["cards"] = Card.objects.order_by('series').all()

    if request.POST:
        if request.POST['action'] == "find_cards":
            form = CardsConditionsForm(request.POST)
            if form.is_valid():
                context["cards"] = form.get_cards()
            else:
                log.error(form.errors.as_data())

        if request.POST['action'] == "renew_statuses":
            form = UpdateStatusesForm(request.POST)
            if form.is_valid():
                form.update()
            else:
                log.error(form.errors.as_data())

    context["cards_conditions_form"] = CardsConditionsForm()
    context["update_statuses_form"] = UpdateStatusesForm()

    return render(request, "cards_find_by.html", context)


@login_required
def cards_generate(request):
    context = dict()

    if request.POST and request.POST['action'] == "generate_cards":
        form = GenerateCardsForm(request.POST)
        if form.is_valid():
            form.generate()
        else:
            log.error(form.errors.as_data())
        return HttpResponseRedirect(reverse('cards_find_by'))

    context["generate_cards_form"] = GenerateCardsForm()

    return render(request, "cards_generate.html", context)


@login_required
def cards_card_edit(request, series, number):
    context = dict()

    if request.POST and request.POST['action'] == "edit_card":
        form = CardEditForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            log.error(form.errors.as_data())

    card = Card.objects.filter(series=series).get(number=number)
    context["card"] = card
    context["purchases"] = Purchase.objects.filter(card=card)

    context["card_edit_form"] = CardEditForm(initial={'status': card.status})

    return render(request, "cards_card_edit.html", context)


@login_required
def cards_card_delete(request, series, number):
    context = dict()

    if request.POST and request.POST['action'] == "delete_card":
        form = CardDeleteForm(request.POST)
        if form.is_valid():
            form.delete(series, number)
        else:
            log.error(form.errors.as_data())
        return HttpResponseRedirect(reverse('cards_find_by'))

    context["card_delete_form"] = CardDeleteForm()

    return render(request, "cards_card_delete.html", context)


