from django.db import models
from datetime import datetime

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
    project_number = models.CharField(
        verbose_name='Project number',
        max_length=33,
        unique=True
    )
    dead_line = models.DateField(verbose_name='Dead line')
    quantity = models.PositiveSmallIntegerField(verbose_name='Quantity')
    project_status = models.CharField(
        choices=STATUS,
        max_length=12,
        default='Preparation'
    )
    cost = models.PositiveIntegerField(
        verbose_name='Global project cost',
        default=0
    )

    def __str__(self):
        return f'{self.customer} nr.{self.project_number}'

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'


class Employees(models.Model):
    name = models.CharField(
        max_length=55,
        verbose_name='Name'
    )
    surname = models.CharField(
        max_length=55,
        verbose_name='Surname'
    )
    salary = models.PositiveSmallIntegerField(
        verbose_name='Salary(zł/h)'
    )

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'


class WorkerProductivity(models.Model):
    worker = models.ForeignKey(
        Employees,
        null=True,
        on_delete=models.SET_NULL
    )
    task = models.ForeignKey(
        'Work',
        null=True,
        on_delete=models.SET_NULL
    )
    time = models.PositiveSmallIntegerField(
        verbose_name='Time in hours'
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Made pieces'
    )
    average_productivity = models.FloatField(
        verbose_name='Average productivity'
    )

    def __str__(self):
        return f'{self.worker} {self.task} productivity'

    class Meta:
        verbose_name = 'Worker productivity'
        verbose_name_plural = 'Workers productivity'


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
    efficiency = models.FloatField(
        default=0,
        verbose_name='Min for piece'
    )
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )
    worker_productivity = models.ForeignKey(
        WorkerProductivity,
        null=True,
        on_delete=models.SET_NULL
    )
    cost = models.IntegerField

    def __str__(self):
        return f'{self.shortcut} - {self.project}'

    class Meta:
        verbose_name = 'Work'
        verbose_name_plural = 'Works'


class Raports(models.Model):
    worker = models.ForeignKey(
        Employees,
        null=True,
        on_delete=models.SET_NULL
    )
    time = models.FloatField(verbose_name='Time')
    quantity = models.PositiveSmallIntegerField(verbose_name='Made pieces')
    date = models.DateField(
        default=datetime.now(),
        verbose_name='Date'
    )
    task = models.ForeignKey(
        Work,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.worker} - {self.task.shortcut} {self.date}'

    class Meta:
        verbose_name = 'Raport'
        verbose_name_plural = 'Raports'


class Expenses(models.Model):
    description = models.CharField(
        max_length=255,
        verbose_name='Expenses'
    )
    quantity = models.PositiveIntegerField(verbose_name='Quantity')
    price = models.FloatField(verbose_name='Price for piece')
    project = models.ForeignKey(
        Projects,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'Expense: {self.description}'

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'



