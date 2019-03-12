from django.db import models


STATUS = (
    ('Preparation', 'Preparation'),
    ('In progress', 'In progress'),
    ('Done', 'Done')
)


class Projects(models.Model):
    customer = models.CharField(
        max_length=55,
        verbose_name='Customer'
    )
    project_number = models.PositiveSmallIntegerField(verbose_name='Project number')
    dead_line = models.DateField(verbose_name='Dead line')
    quantity = models.PositiveSmallIntegerField(verbose_name='Quantity')
    project_status = models.CharField(
        choices=STATUS,
        max_length=12,
        default='Preparation'
    )

    def __str__(self):
        return f'{self.customer} nr.{self.project_number}'

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class Work(models.Model):
    shortcut = models.CharField(
        max_length=5,
        verbose_name='Shortcut'
    )
    description = models.TextField(verbose_name='Description')
    done = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Done'
    )
    efficiency = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Min for piece'
    )
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.shortcut

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'


class ProductionLine(models.Model):
    line_name = models.CharField(
        max_length=55,
        verbose_name='Line name'
    )
    work = models.ForeignKey(
        Work,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.line_name

    class Meta:
        verbose_name = 'Production line'
        verbose_name_plural = 'Production lines'


class Employees(models.Model):
    name = models.CharField(
        max_length=55,
        verbose_name='Name'
    )
    surname = models.CharField(
        max_length=55,
        verbose_name='Surname'
    )
    production_line = models.ForeignKey(
        ProductionLine,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'





