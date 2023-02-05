from django.db import models


class Demand(models.Model):
    year = models.IntegerField("Год")
    med_salary = models.FloatField("Зарплата")
    vac_count = models.IntegerField("Количество вакансий")
    med_salary_python = models.FloatField("Зарплата по выбранной профессии", null=True)
    vac_count_python = models.IntegerField("Количество вакансий по выбранной профессии", null=True)

    def __str__(self):
        return self.year

    class Meta:
        verbose_name = "Востребованность"
        verbose_name_plural = "Востребованность"


class Geography(models.Model):
    city = models.CharField("Город", max_length=20)
    med_salary = models.FloatField("Мединаная зарплата")
    vac_count = models.IntegerField("Количество вакансий")

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = "География"
        verbose_name_plural = "География"
