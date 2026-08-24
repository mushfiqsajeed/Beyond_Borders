"""
URL configuration for Beyond_Borders project.
"""


from django.contrib import admin

from django.urls import path, include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('firstpage.urls')),
    path("scholarship-eligibility/", include("scholarship_eligibility.urls")),
    path("explore-scholarships/", include("explore_scholarships.urls")),
    path("explore-countries/", include("explore_countries.urls")),
    path("profile/", include("user_profile.urls")),
    path("universities/", include("explore_universities.urls")),
]
