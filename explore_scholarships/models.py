from django.db import models


class Scholarship(models.Model):
    university_name = models.CharField(max_length=255)
    scholarship_name = models.CharField(max_length=255)
    degree_level = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_cgpa = models.DecimalField(max_digits=3, decimal_places=2)
    application_deadline = models.DateField()

    pk = models.CompositePrimaryKey(
        "university_name",
        "scholarship_name"
    )

    class Meta:
        managed = False
        db_table = "Scholarship"
