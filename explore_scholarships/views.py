from django.shortcuts import render
from django.db import connection


def scholarship_list(request):

    search = request.GET.get("search", "").strip()
    country = request.GET.get("country", "").strip()
    amount = request.GET.get("amount", "").strip()

    query = """
        SELECT
            s.Scholarship_Name,
            s.university_name,
            u.country_name,
            s.Degree_level,
            s.Amount,
            s.Minimum_cgpa,
            s.Application_deadline
        FROM Scholarship s
        JOIN University u
            ON s.university_name = u.university_name
        WHERE 1=1
    """

    params = []

    # Search by scholarship name OR university
    if search:
        query += """
            AND (
                s.Scholarship_Name LIKE %s
                OR s.university_name LIKE %s
            )
        """

        params.append(f"%{search}%")
        params.append(f"%{search}%")

    # Filter by country
    if country:
        query += """
            AND u.country_name = %s
        """

        params.append(country)

    # Filter by amount
    if amount == "under_10000":
        query += """
            AND s.Amount < 10000
        """

    elif amount == "10000_25000":
        query += """
            AND s.Amount >= 10000
            AND s.Amount < 25000
        """

    elif amount == "25000_50000":
        query += """
            AND s.Amount >= 25000
            AND s.Amount <= 50000
        """

    elif amount == "over_50000":
        query += """
            AND s.Amount > 50000
        """

    with connection.cursor() as cursor:
        cursor.execute(query, params)

        columns = [column[0] for column in cursor.description]

        scholarships = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    # Get countries for the country dropdown
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT country_name
            FROM University
            ORDER BY country_name
        """)

        countries = [row[0] for row in cursor.fetchall()]

    return render(
        request,
        "explore_scholarships.html",
        {
            "scholarships": scholarships,
            "search": search,
            "country": country,
            "amount": amount,
            "countries": countries,
        }
    )