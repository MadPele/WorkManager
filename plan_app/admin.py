from django.contrib import admin
from .models import Employees, Work, ProductionLine, Projects


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    pass


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductionLine)
class ProductionLineAdmin(admin.ModelAdmin):
    pass


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    pass

