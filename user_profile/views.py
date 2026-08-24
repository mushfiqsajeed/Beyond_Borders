from django.shortcuts import render, redirect
from django.db import connection


def profile(request):

    email = request.session.get("student_email")

    if not email:
        return redirect("login")

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                Email,
                Full_Name,
                Nationality,
                Phone,
                Current_institution,
                Current_degree,
                cgpa,
                degree_level_sought,
                Field_of_study
            FROM Student
            WHERE Email = %s
            """,
            [email]
        )

        student = cursor.fetchone()

    if student is None:
        return redirect("login")


    # ==========================================
    # PROFILE COMPLETION CALCULATION
    # ==========================================

    profile_fields = [
        student[0],  # Email
        student[1],  # Full Name
        student[2],  # Nationality
        student[3],  # Phone
        student[4],  # Current Institution
        student[5],  # Current Degree
        student[6],  # CGPA
        student[7],  # Degree Level Sought
        student[8],  # Field of Study
    ]

    completed_fields = sum(
        1
        for field in profile_fields
        if field is not None and str(field).strip() != ""
    )

    total_fields = len(profile_fields)

    profile_completion = round(
        (completed_fields / total_fields) * 100
    )


    # ==========================================
    # STANDARDIZED TESTS
    # ==========================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT Test_Name, Score
            FROM Standardized_Test
            WHERE Email = %s
            ORDER BY Test_Name
            """,
            [email]
        )

        tests = cursor.fetchall()


    return render(request, "profile.html", {

        "email": student[0],
        "full_name": student[1],
        "nationality": student[2],
        "phone": student[3],
        "current_institution": student[4],
        "current_degree": student[5],
        "cgpa": student[6],
        "degree_level_sought": student[7],
        "field_of_study": student[8],

        "tests": tests,

        "profile_completion": profile_completion,
    })

def edit_profile(request):

    email = request.session.get("student_email")

    if not email:
        return redirect("login")

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        nationality = request.POST.get("nationality")
        phone = request.POST.get("phone")
        current_institution = request.POST.get("current_institution")
        current_degree = request.POST.get("current_degree")
        cgpa = request.POST.get("cgpa")
        degree_level_sought = request.POST.get("degree_level_sought")
        field_of_study = request.POST.get("field_of_study")

        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE Student
                SET Full_Name = %s,
                    Nationality = %s,
                    Phone = %s,
                    Current_institution = %s,
                    Current_degree = %s,
                    cgpa = %s,
                    degree_level_sought = %s,
                    Field_of_study = %s
                WHERE Email = %s
                """,
                [
                    full_name,
                    nationality,
                    phone,
                    current_institution,
                    current_degree,
                    cgpa,
                    degree_level_sought,
                    field_of_study,
                    email
                ]
            )

        return redirect("profile")

    # GET request → load current information
    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT Email, Full_Name, Nationality, Phone,
                   Current_institution, Current_degree,
                   cgpa, degree_level_sought, Field_of_study
            FROM Student
            WHERE Email = %s
            """,
            [email]
        )

        student = cursor.fetchone()

    if student is None:
        return redirect("login")

    return render(request, "edit_profile.html", {
        "student": student
    })

def update_test_score(request):

    email = request.session.get("student_email")

    if not email:
        return redirect("login")

    if request.method == "POST":

        test_name = request.POST.get("test_name")
        test_score = request.POST.get("test_score")

        if not test_name or not test_score:
            return redirect("profile")

        try:
            test_score = float(test_score)

        except ValueError:
            return redirect("profile")

        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO Standardized_Test
                    (Email, Test_Name, Score)
                VALUES
                    (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    Score = VALUES(Score)
                """,
                [
                    email,
                    test_name,
                    test_score
                ]
            )

    return redirect("profile")