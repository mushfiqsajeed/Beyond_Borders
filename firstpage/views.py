from django.db import connection
from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation
from datetime import date


# =========================================================
# HOMEPAGE
# =========================================================

def hello(request):

    return render(
        request,
        "homepage.html"
    )



# =========================================================
# SIGNUP
# =========================================================

def signup(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")


        if password != confirm_password:

            return render(
                request,
                "signup.html",
                {
                    "error": "Passwords do not match."
                }
            )


        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT Email
                FROM Student
                WHERE Email=%s
                """,
                [email]
            )

            exists = cursor.fetchone()


        if exists:

            return render(
                request,
                "signup.html",
                {
                    "error":
                    "Account already exists."
                }
            )


        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO Student
                (
                    Email,
                    Full_Name,
                    Password
                )

                VALUES
                (
                    %s,
                    %s,
                    %s
                )
                """,
                [
                    email,
                    full_name,
                    password
                ]
            )


        return redirect("login")



    return render(
        request,
        "signup.html"
    )



# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")


        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT Full_Name
                FROM Student
                WHERE Email=%s
                AND Password=%s
                """,
                [
                    email,
                    password
                ]
            )

            student = cursor.fetchone()



        if student:

            request.session["student_email"] = email
            request.session["full_name"] = student[0]


            return redirect(
                "dashboard"
            )


        return render(
            request,
            "login.html",
            {
                "error":
                "Invalid email or password."
            }
        )


    return render(
        request,
        "login.html"
    )



# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    request.session.flush()

    return redirect(
        "login"
    )
# =========================================================
# LOADING PAGE
# =========================================================

def login_loading(request):

    return render(
        request,
        "loading.html"
    )



# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):

    # =====================================================
    # CHECK LOGIN SESSION
    # =====================================================

    email = request.session.get("student_email")
    if "student_email" not in request.session:

        return redirect(
            "login"
        )


    email = request.session["student_email"]



    # =====================================================
    # GET STUDENT INFORMATION
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                Full_Name,
                Nationality,
                Phone,
                Current_institution,
                Current_degree,
                cgpa
            FROM Student
            WHERE Email=%s
            """,
            [
                email
            ]
        )

        student = cursor.fetchone()


    if student is None:
        return redirect("login")


    full_name = student[1]


    # =====================================================
    # PROFILE COMPLETION
    # =====================================================


    full_name = student[0] if student else ""



    completed_fields = sum(
        1
        for field in profile_fields
        if field is not None
        and str(field).strip() != ""
    )


    total_fields = len(profile_fields)


    profile_completion = round(
    completed_fields = 0
    total_fields = 6


    if student:

        for value in student:

            if value:

                completed_fields += 1



    profile_completion = int(
        (completed_fields / total_fields) * 100
    )


    # =====================================================
    # COUNT SAVED UNIVERSITIES
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Saved_University
            WHERE Email = %s
            """,
            [email]
        )

        saved_university_count = cursor.fetchone()[0]


    # =====================================================
    # COUNT SAVED SCHOLARSHIPS
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Saved_Scholarship
            WHERE Email = %s
            """,
            [email]
        )

        saved_scholarship_count = cursor.fetchone()[0]


    # =====================================================
    # RENDER DASHBOARD
    # =====================================================

    return render(
        request,
        "dashboard.html",
        {
            "full_name":
                full_name,

            "profile_completion":
                profile_completion,

            "saved_university_count":
                saved_university_count,

            "saved_scholarship_count":
                saved_scholarship_count,

            "active_page":
                "dashboard",
            "full_name": full_name,
            "profile_completion": profile_completion,
        }
    )



# =========================================================
# ADMISSION REQUIREMENT CHECKER
# =========================================================

def admission_checker(request):

    universities = []


    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT university_name
            FROM University
            """
        )

        rows = cursor.fetchall()


        for row in rows:

            universities.append(
                row[0]
            )



    result = None



    if request.method == "POST":


        selected_university = request.POST.get(
            "university"
        )


        email = request.session.get(
            "student_email"
        )



        with connection.cursor() as cursor:


            cursor.execute(
                """
                SELECT
                    minimum_cgpa,
                    IELTS_score_required,
                    TOEFL_score_required,
                    PTE_score_required,
                    GRE_score_required,
                    GMAT_score_required,
                    SAT_score_required,
                    documents_required

                FROM Admission_Requirements

                WHERE university_name=%s

                """,
                [
                    selected_university
                ]
            )


            requirement = cursor.fetchone()



            cursor.execute(
                """
                SELECT cgpa
                FROM Student
                WHERE Email=%s
                """,
                [
                    email
                ]
            )


            student_data = cursor.fetchone()



        if requirement:


            student_cgpa = (
                student_data[0]
                if student_data
                else None
            )


            minimum_cgpa = requirement[0]



            cgpa_status = (
                "fulfilled"
                if student_cgpa
                and student_cgpa >= minimum_cgpa
                else "not_fulfilled"
            )



            tests = [

                {
                    "name": "IELTS",
                    "required": requirement[1],
                    "student_score": None,
                    "status": "not_provided"
                },

                {
                    "name": "TOEFL",
                    "required": requirement[2],
                    "student_score": None,
                    "status": "not_provided"
                },

                {
                    "name": "PTE",
                    "required": requirement[3],
                    "student_score": None,
                    "status": "not_provided"
                },

                {
                    "name": "GRE",
                    "required": requirement[4],
                    "student_score": None,
                    "status": "not_provided"
                },

                {
                    "name": "GMAT",
                    "required": requirement[5],
                    "student_score": None,
                    "status": "not_provided"
                },

                {
                    "name": "SAT",
                    "required": requirement[6],
                    "student_score": None,
                    "status": "not_provided"
                }

            ]



            fulfilled_count = 0


            if cgpa_status == "fulfilled":

                fulfilled_count += 1



            total_requirements = 7



            match_percentage = int(
                (fulfilled_count / total_requirements) * 100
            )



            result = {

                "university":
                    selected_university,

                "minimum_cgpa":
                    minimum_cgpa,

                "student_cgpa":
                    student_cgpa,

                "cgpa_status":
                    cgpa_status,

                "tests":
                    tests,

                "documents":
                    requirement[7],

                "fulfilled_count":
                    fulfilled_count,

                "total_requirements":
                    total_requirements,

                "needs_attention":
                    total_requirements - fulfilled_count,

                "match_percentage":
                    match_percentage
            }



    return render(
        request,
        "admission_checker.html",
        {
            "universities": universities,
            "result": result
        }
    )
# =========================================================
# COST ESTIMATOR
# =========================================================

def cost_estimator(request):

    universities = []
    countries = []


    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT university_name
            FROM University
            """
        )

        universities = [
            row[0]
            for row in cursor.fetchall()
        ]



        cursor.execute(
            """
            SELECT country_name
            FROM Country
            """
        )

        countries = [
            row[0]
            for row in cursor.fetchall()
        ]



    result = None



    if request.method == "POST":


        university = request.POST.get(
            "university"
        )

        country = request.POST.get(
            "country"
        )


        calculation_mode = request.POST.get(
            "calculation_mode"
        )


        other_expenses = request.POST.get(
            "other_expenses"
        )



        try:

            other_expenses = Decimal(
                other_expenses
                if other_expenses
                else "0"
            )

        except InvalidOperation:

            other_expenses = Decimal("0")



        with connection.cursor() as cursor:


            if calculation_mode == "university" and university:


                cursor.execute(
                    """
                    SELECT
                        U.university_name,
                        U.country_name,
                        U.tuition_fee,
                        U.world_ranking,

                        C.accommodation_cost,
                        C.grocery_cost,
                        C.transportation_cost,
                        C.climate,
                        C.healthcare_info,
                        C.student_lifestyle

                    FROM University U

                    JOIN Country C

                    ON U.country_name=C.country_name

                    WHERE U.university_name=%s

                    """,
                    [
                        university
                    ]
                )



            else:


                cursor.execute(
                    """
                    SELECT
                        U.university_name,
                        U.country_name,
                        U.tuition_fee,
                        U.world_ranking,

                        C.accommodation_cost,
                        C.grocery_cost,
                        C.transportation_cost,
                        C.climate,
                        C.healthcare_info,
                        C.student_lifestyle

                    FROM University U

                    JOIN Country C

                    ON U.country_name=C.country_name

                    WHERE U.country_name=%s

                    LIMIT 1

                    """,
                    [
                        country
                    ]
                )



            data = cursor.fetchone()



        if data:


            monthly_living = (
                Decimal(data[4])
                +
                Decimal(data[5])
                +
                Decimal(data[6])
                +
                other_expenses
            )


            yearly_living = (
                monthly_living * 12
            )


            yearly_total = (
                Decimal(data[2])
                +
                yearly_living
            )



            result = {

                "university":
                    data[0],

                "country":
                    data[1],

                "tuition_fee":
                    data[2],

                "world_ranking":
                    data[3],

                "monthly_accommodation":
                    data[4],

                "monthly_food":
                    data[5],

                "monthly_transport":
                    data[6],

                "monthly_living_total":
                    monthly_living,

                "yearly_living_cost":
                    yearly_living,

                "estimated_yearly_total":
                    yearly_total,

                "climate":
                    data[7],

                "healthcare_info":
                    data[8],

                "student_lifestyle":
                    data[9]

            }



    return render(
        request,
        "cost_estimator.html",
        {
            "universities": universities,
            "countries": countries,
            "result": result
        }
    )





def document_review(request):

    from django.shortcuts import render
    from django.db import connection


    # ===============================
    # LOAD EXPERT DATA
    # ===============================

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                id,
                name,
                specialization,
                experience,
                rating,
                country
            FROM firstpage_expert
        """)

        expert_rows = cursor.fetchall()



    experts = []


    for expert in expert_rows:

        experts.append({

            "id": expert[0],

            "name": expert[1],

            "specialization": expert[2],

            "experience": expert[3],

            "rating": expert[4],

            "country": expert[5],

        })



    # ===============================
    # HANDLE SUBMISSION
    # NO DATABASE SAVE
    # ===============================

    success = None


    if request.method == "POST":

        success = (
            "Your document review request has been submitted successfully. "
            "Your request is pending expert review."
        )



    # ===============================
    # SEND DATA TO TEMPLATE
    # ===============================

    context = {

        "experts": experts,

        "success": success,

    }



    return render(
        request,
        "document_review.html",
        context
    )