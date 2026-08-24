from django.shortcuts import render
from django.db import connection


def explore_countries(request):

    search = request.GET.get("search", "").strip()

    query = """
        SELECT
            country_name,
            climate,
            student_lifestyle,
            accommodation_cost,
            grocery_cost,
            transportation_cost
        FROM Country
    """

    params = []

    if search:
        query += """
            WHERE country_name LIKE %s
        """

        params.append(f"%{search}%")

    query += """
        ORDER BY country_name
    """

    with connection.cursor() as cursor:
        cursor.execute(query, params)

        columns = [column[0] for column in cursor.description]

        countries = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    return render(
        request,
        "explore_countries.html",
        {
            "countries": countries,
            "search": search,
        }
    )


def country_detail(request, country_name):

    query = """
        SELECT
            country_name,
            climate,
            student_lifestyle,
            visa_information,
            accommodation_cost,
            grocery_cost,
            transportation_cost,
            healthcare_info,
            work_opportunities
        FROM Country
        WHERE country_name = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [country_name])

        row = cursor.fetchone()

        if row:
            columns = [column[0] for column in cursor.description]
            country = dict(zip(columns, row))
        else:
            country = None

    if country is None:
        return render(
            request,
            "country_detail.html",
            {
                "country": None,
                "not_found": True,
            },
            status=404
        )

    return render(
        request,
        "country_detail.html",
        {
            "country": country,
            "not_found": False,
        }
    )