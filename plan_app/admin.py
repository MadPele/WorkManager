from django.contrib import admin
from .models import Employees, Work, Projects, Raports, WorkerProductivity, Expenses


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkerProductivity)
class WorkerProductivityAdmin(admin.ModelAdmin):
    pass


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    pass


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    pass


@admin.register(Raports)
class RaportsAdmin(admin.ModelAdmin):
    pass


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    pass