from django.db import models


class Country(models.Model):
    country_name = models.CharField(max_length=100, primary_key=True)
    climate = models.CharField(max_length=100)
    student_lifestyle = models.TextField()
    visa_information = models.TextField()
    accommodation_cost = models.DecimalField(max_digits=10, decimal_places=2)
    grocery_cost = models.DecimalField(max_digits=10, decimal_places=2)
    transportation_cost = models.DecimalField(max_digits=10, decimal_places=2)
    healthcare_info = models.TextField()
    work_opportunities = models.TextField()

    class Meta:
        managed = False
        db_table = "Country"