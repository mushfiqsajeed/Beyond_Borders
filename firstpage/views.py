from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse

# Create your views here.
#Request -> response

def hello (request):
    return render (request, 'homepage.html') 

def signup(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check whether passwords match
        if password != confirm_password:

            return render(request, "signup.html", {
                "error": "Passwords do not match."
            })

        # Check whether email already exists
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT Email
                FROM Student
                WHERE Email = %s
                """,
                [email]
            )

            existing_student = cursor.fetchone()

        if existing_student:

            return render(request, "signup.html", {
                "error": "An account with this email already exists."
            })

        # Insert new student
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO Student
                    (Email, Full_Name, Password)
                VALUES
                    (%s, %s, %s)
                """,
                [email, full_name, password]
            )

        # Signup successful
        return redirect("login")

    return render(request, "signup.html")


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT Email, Password
                FROM Student
                WHERE Email = %s
                """,
                [email]
            )

            student = cursor.fetchone()

        if student is None:

            return render(request, "login.html", {
                "error": "Invalid email or password."
            })

        stored_password = student[1]

        if password != stored_password:

            return render(request, "login.html", {
                "error": "Invalid email or password."
            })

        request.session["student_email"] = email

        return redirect("login_loading")

    # This handles GET requests
    return render(request, "login.html")

#= = = Dashboard = = =#
def dashboard(request):

    email = request.session.get("student_email")

    if not email:
        return redirect("login")

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT Full_Name
            FROM Student
            WHERE Email = %s
            """,
            [email]
        )

        student = cursor.fetchone()

    if student is None:
        return redirect("login")

    full_name = student[0]

    return render(request, "dashboard.html", {
        "full_name": full_name
    })

def login_loading(request):
    return render(request, "loading.html")