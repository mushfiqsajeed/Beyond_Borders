from django.db import connection
from django.shortcuts import render, redirect


def saved_home(request):

    email = request.session.get("student_email")

    if not email:
        return redirect("login")

    return render(
        request,
        "saved.html",
        {
            "active_page": "saved",
        }
    )


def saved_universities(request):

    email = request.session.get("student_email")

    if not email:
        return redirect("login")


    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                U.university_name,
                U.country_name,
                U.tuition_fee,
                U.application_deadline,
                U.world_ranking

            FROM Saved_University SU

            JOIN University U
                ON SU.university_name = U.university_name

            WHERE SU.Email = %s

            ORDER BY U.world_ranking ASC
            """,
            [email]
        )

        rows = cursor.fetchall()


    universities = []

    for row in rows:

        universities.append(
            {
                "university_name": row[0],
                "country_name": row[1],
                "tuition_fee": row[2],
                "application_deadline": row[3],
                "world_ranking": row[4],
            }
        )


    return render(
        request,
        "saved_universities.html",
        {
            "universities": universities,
            "active_page": "saved",
        }
    )

def toggle_saved_university(request):

    email = request.session.get("student_email")

    if not email:
        return redirect("login")


    if request.method != "POST":
        return redirect("explore_universities")


    university_name = request.POST.get(
        "university_name",
        ""
    ).strip()


    if not university_name:
        return redirect("explore_universities")


    with connection.cursor() as cursor:

        # Check whether this university
        # is already saved by this student

        cursor.execute(
            """
            SELECT 1
            FROM Saved_University
            WHERE Email = %s
              AND university_name = %s
            """,
            [
                email,
                university_name
            ]
        )

        already_saved = cursor.fetchone()


        # If already saved -> remove it

        if already_saved:

            cursor.execute(
                """
                DELETE FROM Saved_University
                WHERE Email = %s
                  AND university_name = %s
                """,
                [
                    email,
                    university_name
                ]
            )


        # Otherwise -> save it

        else:

            cursor.execute(
                """
                INSERT INTO Saved_University
                    (Email, university_name)
                VALUES
                    (%s, %s)
                """,
                [
                    email,
                    university_name
                ]
            )


    # Return to the same Explore Universities page
    # including the current search/sort settings

    next_url = request.POST.get(
        "next",
        ""
    )


    if next_url.startswith("/"):

        return redirect(next_url)


    return redirect("explore_universities")

def saved_scholarships(request):

    # =====================================================
    # CHECK LOGIN SESSION
    # =====================================================

    email = request.session.get("student_email")

    if not email:
        return redirect("login")


    # =====================================================
    # FETCH THIS STUDENT'S SAVED SCHOLARSHIPS
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                S.Scholarship_Name,
                S.university_name,
                U.country_name,
                S.Degree_level,
                S.Amount,
                S.Minimum_cgpa,
                S.Application_deadline

            FROM Saved_Scholarship SS

            JOIN Scholarship S
                ON SS.university_name = S.university_name
                AND SS.Scholarship_Name = S.Scholarship_Name

            JOIN University U
                ON S.university_name = U.university_name

            WHERE SS.Email = %s

            ORDER BY S.Application_deadline ASC
            """,
            [email]
        )


        rows = cursor.fetchall()


    # =====================================================
    # CONVERT DATABASE ROWS INTO DICTIONARIES
    # =====================================================

    scholarships = []


    for row in rows:

        scholarships.append(
            {
                "Scholarship_Name":
                    row[0],

                "university_name":
                    row[1],

                "country_name":
                    row[2],

                "Degree_level":
                    row[3],

                "Amount":
                    row[4],

                "Minimum_cgpa":
                    row[5],

                "Application_deadline":
                    row[6],
            }
        )


    # =====================================================
    # RENDER PAGE
    # =====================================================

    return render(
        request,
        "saved_scholarships.html",
        {
            "scholarships": scholarships,
            "active_page": "saved",
        }
    )

def toggle_saved_scholarship(request):

    # =====================================================
    # CHECK LOGIN SESSION
    # =====================================================

    email = request.session.get("student_email")

    if not email:
        return redirect("login")


    # =====================================================
    # ONLY ALLOW POST
    # =====================================================

    if request.method != "POST":
        return redirect("scholarship_list")


    # =====================================================
    # GET SCHOLARSHIP INFORMATION
    # =====================================================

    university_name = request.POST.get(
        "university_name",
        ""
    ).strip()


    scholarship_name = request.POST.get(
        "scholarship_name",
        ""
    ).strip()


    if not university_name or not scholarship_name:
        return redirect("scholarship_list")


    # =====================================================
    # CHECK WHETHER ALREADY SAVED
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT 1

            FROM Saved_Scholarship

            WHERE Email = %s
              AND university_name = %s
              AND Scholarship_Name = %s
            """,
            [
                email,
                university_name,
                scholarship_name
            ]
        )


        already_saved = cursor.fetchone()


        # =================================================
        # IF ALREADY SAVED -> DELETE
        # =================================================

        if already_saved:

            cursor.execute(
                """
                DELETE FROM Saved_Scholarship

                WHERE Email = %s
                  AND university_name = %s
                  AND Scholarship_Name = %s
                """,
                [
                    email,
                    university_name,
                    scholarship_name
                ]
            )


        # =================================================
        # OTHERWISE -> INSERT
        # =================================================

        else:

            cursor.execute(
                """
                INSERT INTO Saved_Scholarship
                    (
                        Email,
                        university_name,
                        Scholarship_Name
                    )

                VALUES
                    (%s, %s, %s)
                """,
                [
                    email,
                    university_name,
                    scholarship_name
                ]
            )


    # =====================================================
    # RETURN TO SAME PAGE
    # =====================================================

    next_url = request.POST.get(
        "next",
        ""
    )


    if next_url.startswith("/"):

        return redirect(next_url)


    return redirect("scholarship_list")