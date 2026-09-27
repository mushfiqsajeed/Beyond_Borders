from django.shortcuts import render, redirect
from django.db import connection


def document_review(request):

    # =====================================================
    # AUTHENTICATION
    # =====================================================

    email = request.session.get("student_email")

    if not email:
        return redirect("login")


    # =====================================================
    # LOAD EXPERT DATA
    # =====================================================

    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                Mentor_Email,
                Full_Name,
                Field_of_Study,
                Current_Institution,
                Highest_Degree
            FROM Mentor
        """)

        expert_rows = cursor.fetchall()


    experts = []

    for expert in expert_rows:

        experts.append({
            "Mentor_Email": expert[0],
            "Full_Name": expert[1],
            "Field_of_Study": expert[2],
            "Current_Institution": expert[3],
            "Highest_Degree": expert[4],
        })


    # =====================================================
    # HANDLE SUBMISSION
    # =====================================================

    success = None

    if request.method == "POST":

        expert_email = request.POST.get("expert_id")
        documents = request.FILES.getlist("documents")

        # Currently no database save.
        # This preserves the existing feature behavior.

        success = (
            "Your document review request has been submitted successfully. "
            "Your request is pending expert review."
        )


    # =====================================================
    # RENDER PAGE
    # =====================================================

    return render(
        request,
        "document_review.html",
        {
            "experts": experts,
            "success": success,
            "active_page": "document_review",
        }
    )