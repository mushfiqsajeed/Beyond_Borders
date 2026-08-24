"""
URL configuration for Beyond_Borders project.
"""


from django.contrib import admin

from django.urls import path, include



urlpatterns = [


    # Admin

    path(
        "admin/",
        admin.site.urls
    ),



    # Main Application

    path(
        "",
        include("firstpage.urls")
    ),



    # Scholarship Eligibility

    path(
        "scholarship-eligibility/",
        include("scholarship_eligibility.urls")
    ),



    # Explore Scholarships

    path(
        "explore-scholarships/",
        include("explore_scholarships.urls")
    ),



    # Explore Countries

    path(
        "explore-countries/",
        include("explore_countries.urls")
    ),



    # Profile

    path(
        "profile/",
        include("user_profile.urls")
    ),



    # Universities

    path(
        "universities/",
        include("explore_universities.urls")
    ),


]