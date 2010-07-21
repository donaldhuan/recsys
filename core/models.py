from django.db import models
from django.contrib import admin

# Create your models here.
class Genre(models.Model):
    title = models.TextField()
    def __unicode__(self):
        return self.title

class Movie(models.Model):
    title = models.TextField()
    genre = models.ManyToManyField(Genre)
    date = models.DateField()
    def __unicode__(self):
        return self.title

class Occupation(models.Model):
    title = models.TextField()
    def __unicode__(self):
        return self.title

class User(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length = 1, choices = (('M', 'Male'), ('F', 'Female')))
    occupation = models.ForeignKey(Occupation)
    def __unicode__(self):
        return str(self.id)

class Rating(models.Model):
    user = models.ForeignKey(User)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField()
    timestamp = models.DateTimeField()
    def __unicode__(self):
        return str(self.rating)

class Similarity(models.Model):
    similarity = models.FloatField()

try:
    admin.site.register(Genre)
    admin.site.register(Movie)
    admin.site.register(Occupation)
    admin.site.register(User)
    admin.site.register(Rating)
except:
    pass
