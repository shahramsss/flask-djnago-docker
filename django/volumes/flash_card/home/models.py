from django.db import models


class FlashCard(models.Model):
    word = models.CharField(max_length=512)
    meaning = models.CharField(max_length=512)
    example = models.CharField(max_length=1024, null=True, blank=True)
    rate = models.SmallIntegerField(default=0)
    last_reply = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    next_review_date = models.DateField()

    def __str__(self):
        return f"{self.word} - {self.meaning}"