from django.db import models


# Private Models
class MajorCourse(models.Model):
    major = models.ForeignKey('basicInfo.Major', null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey('basicInfo.Course', null=True, on_delete=models.SET_NULL)
    compulsory = models.BooleanField()

class Curriculum(models.Model):
    student = models.ForeignKey('basicInfo.Student', null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey('basicInfo.Course', null=True, on_delete=models.SET_NULL)

class CurriculumDemand(models.Model):
    major = models.ForeignKey('basicInfo.Major', null=True, on_delete=models.SET_NULL)
    elective = models.IntegerField()
    public = models.IntegerField()


class Selection(models.Model):
    student = models.ForeignKey('basicInfo.Student', null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey('courseArrange.Section', null=True, on_delete=models.SET_NULL)
    selection_round = models.IntegerField()
    select_time = models.DateTimeField(null=True)
    drop_time = models.DateTimeField(null=True)
    priority = models.IntegerField()
    selection_condition = models.IntegerField()

    class Meta:
        unique_together = ('section', 'student')


class SelectionTime(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    selection_round = models.IntegerField()

    class Meta:
        unique_together = ('semester', 'year', 'selection_round')


class Constants(models.Model):
    name = models.CharField(max_length=50)
    value = models.FloatField()
