from django.db import models


class Note(models.Model):
    title = models.CharField("Название", max_length=200)
    content = models.TextField("Текст")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    def __str__(self):
        return self.title