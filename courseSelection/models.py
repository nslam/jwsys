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
    compulsory = models.IntegerField()
    elective = models.IntegerField()
    public = models.IntegerField()


class Selection(models.Model):
    student = models.ForeignKey('basicInfo.Student', null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey('courseArrange.Section', null=True, on_delete=models.SET_NULL)
    selection_round = models.IntegerField()
    select_time = models.TimeField()
    drop_time = models.TimeField(null=True)
    priority = models.IntegerField()
    condition = models.IntegerField()


class SelectionTime(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    selection_round = models.IntegerField()


class Constants(models.Model):
    name = models.CharField(max_length=50)
    value = models.FloatField()
