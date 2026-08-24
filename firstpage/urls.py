from django.urls import path
from . import views


urlpatterns = [

    # ==========================
    # Homepage
    # ==========================

    path(
        '',
        views.hello,
        name='home'
    ),


    # ==========================
    # Authentication
    # ==========================

    path(
        'login/',
        views.login_view,
        name='login'
    ),


    path(
        'signup/',
        views.signup,
        name='signup'
    ),


    path(
        'loading/',
        views.login_loading,
        name='login_loading'
    ),



    # ==========================
    # Dashboard
    # ==========================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),



    # ==========================
    # Logout
    # ==========================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),



    # ==========================
    # Feature 1
    # Admission Requirement Checker
    # ==========================

    path(
        'admission-checker/',
        views.admission_checker,
        name='admission_checker'
    ),



    # ==========================
    # Feature 2
    # Cost Estimation Calculator
    # ==========================

    path(
        'cost-estimator/',
        views.cost_estimator,
        name='cost_estimator'
    ),



    # ==========================
    # Feature 3
    # Document Review by Expert
    # ==========================

    path(
        'document-review/',
        views.document_review,
        name='document_review'
    ),

]