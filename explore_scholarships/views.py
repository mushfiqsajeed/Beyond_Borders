from django.shortcuts import render, redirect
from django.db import connection


def scholarship_list(request):

    # =====================================================
    # CHECK LOGIN SESSION
    # =====================================================

    email = request.session.get("student_email")

    if not email:
        return redirect("login")


    # =====================================================
    # GET SEARCH / FILTER VALUES
    # =====================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()


    country = request.GET.get(
        "country",
        ""
    ).strip()


    amount = request.GET.get(
        "amount",
        ""
    ).strip()


    # =====================================================
    # BASE SCHOLARSHIP QUERY
    # =====================================================

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


    # =====================================================
    # SEARCH BY SCHOLARSHIP NAME OR UNIVERSITY
    # =====================================================

    if search:

        query += """
            AND (
                s.Scholarship_Name LIKE %s
                OR s.university_name LIKE %s
            )
        """


        params.append(
            f"%{search}%"
        )

        params.append(
            f"%{search}%"
        )


    # =====================================================
    # FILTER BY COUNTRY
    # =====================================================

    if country:

        query += """
            AND u.country_name = %s
        """

        params.append(
            country
        )


    # =====================================================
    # FILTER BY AMOUNT
    # =====================================================

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


    # =====================================================
    # FETCH SCHOLARSHIPS
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            query,
            params
        )


        columns = [
            column[0]
            for column in cursor.description
        ]


        scholarships = [

            dict(
                zip(
                    columns,
                    row
                )
            )

            for row in cursor.fetchall()
        ]


    # =====================================================
    # FETCH THIS STUDENT'S SAVED SCHOLARSHIPS
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                university_name,
                Scholarship_Name

            FROM Saved_Scholarship

            WHERE Email = %s
            """,
            [email]
        )


        saved_rows = cursor.fetchall()


    # =====================================================
    # CREATE SET OF SAVED SCHOLARSHIP KEYS
    # =====================================================

    saved_scholarship_keys = {

        (
            row[0],
            row[1]
        )

        for row in saved_rows
    }


    # =====================================================
    # ADD is_saved TO EACH SCHOLARSHIP
    # =====================================================

    for scholarship in scholarships:

        scholarship_key = (
            scholarship["university_name"],
            scholarship["Scholarship_Name"]
        )


        scholarship["is_saved"] = (
            scholarship_key
            in saved_scholarship_keys
        )


    # =====================================================
    # GET COUNTRIES FOR COUNTRY DROPDOWN
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT DISTINCT
                country_name

            FROM University

            ORDER BY country_name
            """
        )


        countries = [

            row[0]

            for row in cursor.fetchall()
        ]


    # =====================================================
    # RENDER PAGE
    # =====================================================

    return render(
        request,
        "explore_scholarships.html",
        {

            "scholarships":
                scholarships,

            "search":
                search,

            "country":
                country,

            "amount":
                amount,

            "countries":
                countries,

            "active_page":
                "scholarships",

            "current_url":
                request.get_full_path(),
        }
    )