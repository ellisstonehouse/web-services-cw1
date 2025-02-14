from django.db import models

# Create your models here.
class Professor(models.Model):
    ID = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(primary_key=True, max_length=200)
    email = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.username
    
class Module(models.Model):
    ID = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class ModuleInstance(models.Model):
    ID = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.IntegerField()

    def __str__(self):
        return f"{self.module.name} - Sem {self.semester}, {self.year} "
    

class TaughtModule(models.Model):
    ID = models.AutoField(primary_key=True)
    moduleInstance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.moduleInstance.module.name} - Sem {self.moduleInstance.semester}, {self.moduleInstance.year}, {self.professor.name} "


class Rating(models.Model):
    ID = models.AutoField(primary_key=True)
    taughtModule = models.ForeignKey(TaughtModule, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return str(self.ID)