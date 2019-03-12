from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Projects, ProductionLine, Work, Employees


class HomeView(View):
    """Home page with view on on projects in progress"""

    def get(self, request):
        projects = Projects.objects.filter(project_status='In progress')
        progress = []
        d_line = []
        x = 0
        for project in projects:
            for num in Work.objects.filter(project=project):
                x += num.done
            x = (x/project.quantity*(Work.objects.filter(project=project).count()))*100
            progress.append('Progress: '+str(round(x, 2))+'%')
            d_line.append('Dead line: '+str(project.dead_line))
        result = zip(projects, progress, d_line)
        resultSet = set(result)

        return render(request, 'home.html', {'resultSet': resultSet})


class ProjectCreateView(CreateView):
    """Create new project"""
    model = Projects
    fields = '__all__'

    def get_success_url(self):

        return reverse('project-details', kwargs={'pk': self.object.pk})


class EmployeeCreateView(CreateView):
    """Add new employee"""
    model = Employees
    fields = '__all__'
    success_url = '/employeesite'


class WorkCreateView(CreateView):
    """Add new work to project"""
    model = Work
    fields = '__all__'

    def get_success_url(self):

        task = self.object
        return reverse('project-details', kwargs={'pk': task.project.id})


class ProductionLineCreateView(CreateView):
    """Create new production line"""
    model = ProductionLine
    fields = '__all__'
    success_url = '/'


class ProjectSiteView(View):
    """Site with projects, where you can edit, delete or just show details of project"""

    def get(self, request):
        projects = Projects.objects.all().order_by()
        return render(request, 'project_site.html', {'projects': projects})


class ProjectDetailsView(View):

    def get(self, request, pk):
        project = Projects.objects.get(pk=pk)
        tasks = Work.objects.filter(project__pk=pk)
        if tasks:
            sum_progress = 0
            sum_time = 0
            for work in tasks:
                sum_time += (project.quantity-work.done)*work.efficiency
                sum_progress += work.done
            sum_progress = (sum_progress/(project.quantity*tasks.count()))*100
            sum_progress = round(sum_progress, 2)
            sum_time = round(sum_time/60, 2)
        else:
            sum_progress = 0
            sum_time = 'Unknown'
        return render(request, 'project_details.html', {'project': project, 'tasks': tasks, 'progress': sum_progress,
                                                        'sum_time': sum_time})


class ProjectDeleteView(DeleteView):
    """Delete project"""
    model = Projects
    success_url = '/projectsite'


class ProjectEditView(UpdateView):
    """Edit project"""
    model = Projects
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_success_url(self):

        return reverse('project-details', kwargs={'pk': self.object.pk})


class EmployeeSiteView(View):

    def get(self, request):
        employees = Employees.objects.all().order_by('name')
        return render(request, 'employees_site.html', {'employees': employees})


class EmployeeDeleteView(DeleteView):
    """Delete employee"""
    model = Employees
    success_url = '/employeesite'


class EmployeeEditView(UpdateView):
    """Edit employee's data"""
    model = Employees
    fields = '__all__'
    template_name_suffix = '_update_form'


class WorkDeleteView(DeleteView):
    """Remove work from project"""

    model = Work

    def get_success_url(self):

        task = self.object
        return reverse('project-details', kwargs={'pk': task.project.id})


class WorkEditView(UpdateView):
    """Edit work"""

    model = Work
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_success_url(self):

        task = self.object
        return reverse('project-details', kwargs={'pk': task.project.id})


class ProductionLineSiteView(View):

    def get(self, request):
        productionlines = ProductionLine.objects.all().order_by('line_name')
        return render(request, 'productionline_site.html', {'productionlines': productionlines})


class ProductionLineDeleteView(DeleteView):
    """Delete project"""
    model = ProductionLine
    success_url = '/'
