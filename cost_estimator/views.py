from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation
from datetime import date
# Create your views here.

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