from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=200)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    profilePicture = models.ImageField(
        default="..media.default.png", blank=True, upload_to='employee-profiles')
    userType = models.IntegerField(default=0)

    @property
    def fullName(self):
        return self.firstName + " " + self.lastName

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        try:
            self.name
            return self.name
        except:
            return self.fullName + " " + str(self.id)


class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    @property
    def numbOfEmployees(self):
        return self.employeeS.count()

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        if self.name:
            return self.name + " " + str(self.id)


class Title(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "Title " + str(self.id)