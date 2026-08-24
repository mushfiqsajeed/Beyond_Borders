from django.shortcuts import render
from django.db import connection


def scholarship_eligibility(request):

    # ------------------------------------------
    # GET COUNTRIES
    # ------------------------------------------

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT country_name
            FROM Country
            ORDER BY country_name
        """)

        columns = [column[0] for column in cursor.description]

        countries = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    # ------------------------------------------
    # FIRST VISIT -> SHOW FORM
    # ------------------------------------------

    if request.method != "POST":
        return render(
            request,
            "scholarship_eligibility.html",
            {
                "countries": countries,
                "active_page": "eligibility",
            }
        )

    # ------------------------------------------
    # GET USER INPUT
    # ------------------------------------------

    country = request.POST.get("country", "").strip()
    degree_level = request.POST.get("degree_level", "").strip()
    field_of_study = request.POST.get("field_of_study", "").strip()
    graduation_year = request.POST.get("graduation_year", "").strip()

    cgpa = request.POST.get("cgpa", "").strip()

    ielts_score = request.POST.get("ielts_score", "").strip()
    toefl_score = request.POST.get("toefl_score", "").strip()
    pte_score = request.POST.get("pte_score", "").strip()

    sat_score = request.POST.get("sat_score", "").strip()
    gre_score = request.POST.get("gre_score", "").strip()
    gmat_score = request.POST.get("gmat_score", "").strip()

    # ------------------------------------------
    # CONVERT SCORES
    # ------------------------------------------

    def to_float(value):
        if not value:
            return None

        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    student_cgpa = to_float(cgpa)

    student_ielts = to_float(ielts_score)
    student_toefl = to_float(toefl_score)
    student_pte = to_float(pte_score)

    student_sat = to_float(sat_score)
    student_gre = to_float(gre_score)
    student_gmat = to_float(gmat_score)

    # ------------------------------------------
    # GET SCHOLARSHIPS
    # ------------------------------------------

    query = """
        SELECT
            s.Scholarship_Name,
            s.university_name,
            u.country_name,
            s.Degree_level,
            s.Amount,
            s.Minimum_cgpa,
            s.Application_deadline,

            ar.minimum_cgpa AS admission_minimum_cgpa,

            ar.IELTS_score_required,
            ar.TOEFL_score_required,
            ar.PTE_score_required,

            ar.GRE_score_required,
            ar.GMAT_score_required,
            ar.SAT_score_required

        FROM Scholarship s

        JOIN University u
            ON s.university_name = u.university_name

        LEFT JOIN Admission_Requirements ar
            ON s.university_name = ar.university_name

        WHERE u.country_name = %s

        ORDER BY s.Amount DESC
    """

    with connection.cursor() as cursor:

        cursor.execute(
            query,
            [country]
        )

        columns = [
            column[0]
            for column in cursor.description
        ]

        scholarships = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    # ------------------------------------------
    # RESULT LISTS
    # ------------------------------------------

    eligible = []
    possible = []
    not_eligible = []

    # ------------------------------------------
    # CHECK EACH SCHOLARSHIP
    # ------------------------------------------

    for scholarship in scholarships:

        passed_requirements = []
        failed_requirements = []
        missing_requirements = []

        # ======================================
        # DEGREE LEVEL
        # ======================================

        if scholarship["Degree_level"]:

            if degree_level == scholarship["Degree_level"]:

                passed_requirements.append(
                    "Degree level matches"
                )

            else:

                failed_requirements.append(
                    f"This scholarship is for "
                    f"{scholarship['Degree_level']}"
                )

        # ======================================
        # SCHOLARSHIP CGPA
        # ======================================

        scholarship_cgpa = scholarship["Minimum_cgpa"]

        if scholarship_cgpa is not None:

            if student_cgpa is None:

                missing_requirements.append(
                    "CGPA was not provided"
                )

            elif student_cgpa >= float(scholarship_cgpa):

                passed_requirements.append(
                    "Scholarship CGPA requirement met"
                )

            else:

                failed_requirements.append(
                    f"Your CGPA is below the scholarship requirement "
                    f"of {scholarship_cgpa}"
                )

        # ======================================
        # UNIVERSITY CGPA
        # ======================================

        admission_cgpa = scholarship[
            "admission_minimum_cgpa"
        ]

        if admission_cgpa is not None:

            if student_cgpa is None:

                missing_requirements.append(
                    "Your CGPA is required to check the university admission requirement"
                )

            elif student_cgpa >= float(admission_cgpa):

                passed_requirements.append(
                    "Your CGPA meets the university admission requirement"
                )

            else:

                failed_requirements.append(
                    f"Your CGPA is below the university admission requirement "
                    f"of {admission_cgpa}"
                )

         # ======================================
        # ENGLISH TEST REQUIREMENTS
        # IELTS / TOEFL / PTE
        # ======================================

        english_requirements = []

        if scholarship["IELTS_score_required"] is not None:
            english_requirements.append(
                (
                    "IELTS",
                    float(scholarship["IELTS_score_required"]),
                    student_ielts
                )
            )

        if scholarship["TOEFL_score_required"] is not None:
            english_requirements.append(
                (
                    "TOEFL",
                    float(scholarship["TOEFL_score_required"]),
                    student_toefl
                )
            )

        if scholarship["PTE_score_required"] is not None:
            english_requirements.append(
                (
                    "PTE",
                    float(scholarship["PTE_score_required"]),
                    student_pte
                )
            )

        # --------------------------------------
        # No English test is required
        # --------------------------------------

        if not english_requirements:

            passed_requirements.append(
                "No English proficiency test required"
            )

        else:

            # Tests that the student actually provided
            submitted_english_tests = [
                test
                for test in english_requirements
                if test[2] is not None
            ]

            # ----------------------------------
            # Student provided at least one test
            # ----------------------------------

            if submitted_english_tests:

                english_passed = False

                for (
                    test_name,
                    required_score,
                    student_score
                ) in submitted_english_tests:

                    if student_score >= required_score:

                        english_passed = True

                        passed_requirements.append(
                            f"Your {test_name} score meets the requirement"
                        )

                        break

                # Student provided a test,
                # but none reached the required score

                if not english_passed:

                    failed_requirements.append(
                        "Your English proficiency score does not meet the requirement"
                    )

            # ----------------------------------
            # No required English test provided
            # ----------------------------------

            else:

                missing_requirements.append(
                    "An English proficiency score is required, but you haven't provided one"
                )


        # ======================================
        # STANDARDIZED TEST REQUIREMENTS
        # SAT / GRE / GMAT
        # ======================================

        standardized_requirements = []

        if scholarship["SAT_score_required"] is not None:
            standardized_requirements.append(
                (
                    "SAT",
                    float(scholarship["SAT_score_required"]),
                    student_sat
                )
            )

        if scholarship["GRE_score_required"] is not None:
            standardized_requirements.append(
                (
                    "GRE",
                    float(scholarship["GRE_score_required"]),
                    student_gre
                )
            )

        if scholarship["GMAT_score_required"] is not None:
            standardized_requirements.append(
                (
                    "GMAT",
                    float(scholarship["GMAT_score_required"]),
                    student_gmat
                )
            )

        # --------------------------------------
        # No standardized test is required
        # --------------------------------------

        if not standardized_requirements:

            passed_requirements.append(
                "No standardized test required"
            )

        else:

            # Tests the student actually provided
            submitted_standardized_tests = [
                test
                for test in standardized_requirements
                if test[2] is not None
            ]

            # ----------------------------------
            # Student provided at least one test
            # ----------------------------------

            if submitted_standardized_tests:

                standardized_passed = False

                for (
                    test_name,
                    required_score,
                    student_score
                ) in submitted_standardized_tests:

                    if student_score >= required_score:

                        standardized_passed = True

                        passed_requirements.append(
                            f"Your {test_name} score meets the requirement"
                        )

                        break

                # Student provided tests,
                # but none met the requirement

                if not standardized_passed:

                    failed_requirements.append(
                        "Your standardized test score does not meet the requirement"
                    )

            # ----------------------------------
            # Required standardized test
            # but no score provided
            # ----------------------------------

            else:

                missing_requirements.append(
                    "A standardized test score is required, but you haven't provided one"
                )

        # ======================================
        # SAVE RESULT INFORMATION
        # ======================================

        scholarship["passed_requirements"] = (
            passed_requirements
        )

        scholarship["failed_requirements"] = (
            failed_requirements
        )

        scholarship["missing_requirements"] = (
            missing_requirements
        )

        # ======================================
        # CLASSIFY
        # ======================================

        if failed_requirements:

            scholarship["status"] = "not_eligible"

            not_eligible.append(scholarship)

        elif missing_requirements:

            scholarship["status"] = "possible"

            possible.append(scholarship)

        else:

            scholarship["status"] = "eligible"

            eligible.append(scholarship)

    # ------------------------------------------
    # SHOW RESULTS PAGE
    # ------------------------------------------

    return render(
        request,
        "eligibility_results.html",
        {
            "eligible": eligible,
            "possible": possible,
            "not_eligible": not_eligible,
            "active_page": "eligibility",
        }
    )