from django.db import models


class Submission(models.Model):
    file = models.FileField(upload_to="uploaded-csv/%Y/%m/")

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
