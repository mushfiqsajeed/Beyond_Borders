from django.shortcuts import render, get_object_or_404
from .models import Country


def country_detail(request, country_name):

    country = get_object_or_404(
        Country,
        country_name=country_name
    )

    return render(request, "country_detail.html", {
        "country": country
    })


def explore_countries(request):

    search = request.GET.get("search", "").strip()

    if search:
        countries = Country.objects.filter(
            country_name__icontains=search
        )
    else:
        countries = Country.objects.all()

    return render(request, "explore_countries.html", {
        "countries": countries,
        "search": search,
    })