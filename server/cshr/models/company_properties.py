from django.db import models
from cshr.models.users import User


class CompanyProperties(models.Model):
    name = models.CharField(max_length=45)
    image_of = models.ImageField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Company Property"
        verbose_name_plural = "Company Properties"
