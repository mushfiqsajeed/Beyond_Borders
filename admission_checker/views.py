from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation
from datetime import date
# Create your views here.


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