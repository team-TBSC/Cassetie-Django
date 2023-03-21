from django.db import models

class Selected(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    song1 = models.CharField(max_length=128)
    song2 = models.CharField(max_length=128)
    song3 = models.CharField(max_length=128)
    song4 = models.CharField(max_length=128)
    song5 = models.CharField(max_length=128)

    def __str__(self):
        return self.name

'''
energy{0:low, 1:middle, 2:high}
emotion{0:strong_happy, 1:week_happy, 2:strong_sad, 3:week_sad}
genre{0:락/메탈, 1:발라드, 2:인디/어쿠스틱, 3:트로트, 4:힙합/R&B 5:댄스/POP/일렉트로닉스 6:기타}
'''
class Features(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    energy = models.IntegerField()
    emotion = models.IntegerField()
    genre1 = models.IntegerField()
    genre2 = models.IntegerField()
    genre3 = models.IntegerField()

    def __str__(self):
        return self.name