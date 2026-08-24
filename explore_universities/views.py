from django.db import connection
from django.shortcuts import render, redirect


def explore_universities(request):

    # =====================================================
    # CHECK LOGIN SESSION
    # =====================================================

    email = request.session.get("student_email")

    if not email:
        return redirect("login")


    # =====================================================
    # SEARCH AND SORT
    # =====================================================

    search = request.GET.get(
        "search",
        ""
    ).strip()


    sort_by = request.GET.get(
        "sort_by",
        "ranking"
    )


    # =====================================================
    # ALLOWED SORT OPTIONS
    # =====================================================

    sort_options = {

        "ranking":
            "world_ranking ASC",

        "lowest_cost":
            "tuition_fee ASC",

        "highest_cost":
            "tuition_fee DESC",

        "earliest_deadline":
            "application_deadline ASC",

        "latest_deadline":
            "application_deadline DESC",
    }


    order_by = sort_options.get(
        sort_by,
        "world_ranking ASC"
    )


    # =====================================================
    # OFFICIAL UNIVERSITY WEBSITES
    # =====================================================

    university_websites = {

        "Massachusetts Institute of Technology (MIT)":
            "https://www.mit.edu/",

        "University of Oxford":
            "https://www.ox.ac.uk/",

        "University of Toronto":
            "https://www.utoronto.ca/",

        "University of Melbourne":
            "https://www.unimelb.edu.au/",

        "National University of Singapore (NUS)":
            "https://www.nus.edu.sg/",

        "Seoul National University":
            "https://en.snu.ac.kr/",

        "Tsinghua University":
            "https://www.tsinghua.edu.cn/en/",

        "Technical University of Munich (TUM)":
            "https://www.tum.de/en/",

        "University of Helsinki":
            "https://www.helsinki.fi/en",

        "Delft University of Technology":
            "https://www.tudelft.nl/en/",

        "KTH Royal Institute of Technology":
            "https://www.kth.se/en",

        "ETH Zurich":
            "https://ethz.ch/en.html",
    }


    # =====================================================
    # FETCH UNIVERSITIES
    # =====================================================

    with connection.cursor() as cursor:

        if search:

            sql = f"""
                SELECT
                    university_name,
                    country_name,
                    tuition_fee,
                    application_deadline,
                    world_ranking

                FROM University

                WHERE university_name LIKE %s
                   OR country_name LIKE %s

                ORDER BY {order_by}
            """


            cursor.execute(
                sql,
                [
                    f"%{search}%",
                    f"%{search}%",
                ]
            )


        else:

            sql = f"""
                SELECT
                    university_name,
                    country_name,
                    tuition_fee,
                    application_deadline,
                    world_ranking

                FROM University

                ORDER BY {order_by}
            """


            cursor.execute(sql)


        rows = cursor.fetchall()


    # =====================================================
    # FETCH THIS STUDENT'S SAVED UNIVERSITIES
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                university_name

            FROM Saved_University

            WHERE Email = %s
            """,
            [email]
        )


        saved_rows = cursor.fetchall()


    # Convert the saved university names into a set.
    #
    # Example:
    #
    # {
    #     "University of Oxford",
    #     "ETH Zurich"
    # }

    saved_university_names = {

        row[0]

        for row in saved_rows
    }


    # =====================================================
    # BUILD UNIVERSITY DICTIONARIES
    # =====================================================

    universities = []


    for row in rows:

        university_name = row[0]


        universities.append(
            {

                "university_name":
                    university_name,

                "country_name":
                    row[1],

                "tuition_fee":
                    row[2],

                "application_deadline":
                    row[3],

                "world_ranking":
                    row[4],

                "website_url":
                    university_websites.get(
                        university_name
                    ),

                # True if this university is already
                # saved by the logged-in student.

                "is_saved":
                    university_name
                    in saved_university_names,
            }
        )


    # =====================================================
    # RENDER PAGE
    # =====================================================

    return render(
        request,
        "explore_universities.html",
        {

            "universities":
                universities,

            "search":
                search,

            "sort_by":
                sort_by,

            "active_page":
                "universities",

            # Keeps the current search/sort URL so that
            # after saving we can return to the same page.

            "current_url":
                request.get_full_path(),
        }
    )