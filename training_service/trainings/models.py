from django.db import models


class Training(models.Model):
    user_id = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    duration = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}"


class Exercise(models.Model):
    name = models.CharField(max_length=40)
    weight = models.IntegerField()
    sets = models.IntegerField()
    reps = models.IntegerField()
    rest = models.IntegerField(blank=True, null=True)
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='exercises')

    def __str__(self):
        return f"{self.name} - {self.sets} sets of {self.reps} reps"

