from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Projects, ProductionLine, Work, Employees, Raports
from .forms import RaportForm, LoginForm
from datetime import datetime, date
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import xlsxwriter


class HomeView(LoginRequiredMixin, View):
    """Home page with view on on projects in progress"""
    login_url = '/login'

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


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Create new project"""
    login_url = '/login'

    model = Projects
    fields = '__all__'

    def get_success_url(self):

        return reverse('project-details', kwargs={'pk': self.object.pk})


class EmployeeCreateView(LoginRequiredMixin, CreateView):
    """Add new employee"""
    login_url = '/login'

    model = Employees
    fields = '__all__'
    success_url = '/employeesite'


class WorkCreateView(LoginRequiredMixin, CreateView):
    """Add new work to project"""
    login_url = '/login'

    model = Work
    fields = '__all__'

    def get_success_url(self):

        task = self.object
        return reverse('project-details', kwargs={'pk': task.project.id})


class ProductionLineCreateView(LoginRequiredMixin, CreateView):
    """Create new production line"""
    login_url = '/login'

    model = ProductionLine
    fields = '__all__'
    success_url = '/productionlinesite'


class ProjectSiteView(LoginRequiredMixin, View):
    """Site with projects, where you can edit, delete or just show details of project"""
    login_url = '/login'

    def get(self, request):
        projects = Projects.objects.all().order_by()
        return render(request, 'project_site.html', {'projects': projects})


class ProjectDetailsView(LoginRequiredMixin, View):
    """See details of chosen project"""
    login_url = '/login'

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


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete project"""
    login_url = '/login'

    model = Projects
    success_url = '/projectsite'


class ProjectEditView(LoginRequiredMixin, UpdateView):
    """Edit project"""
    login_url = '/login'

    model = Projects
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_success_url(self):

        return reverse('project-details', kwargs={'pk': self.object.pk})


class EmployeeSiteView(LoginRequiredMixin, View):
    """Show all employees"""
    login_url = '/login'

    def get(self, request):
        employees = Employees.objects.all().order_by('name')
        return render(request, 'employees_site.html', {'employees': employees})


class EmployeeDeleteView(LoginRequiredMixin, DeleteView):
    """Delete employee"""
    login_url = '/login'

    model = Employees
    success_url = '/employeesite'


class EmployeeEditView(LoginRequiredMixin, UpdateView):
    """Edit employee's data"""
    login_url = '/login'

    model = Employees
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_success_url(self):

        return reverse('employee-site')


class WorkDeleteView(LoginRequiredMixin, DeleteView):
    """Remove work from project"""
    login_url = '/login'

    model = Work

    def get_success_url(self):

        task = self.object
        return reverse('project-details', kwargs={'pk': task.project.id})


class WorkEditView(LoginRequiredMixin, UpdateView):
    """Edit work"""
    login_url = '/login'

    model = Work
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_success_url(self):

        task = self.object
        return reverse('project-details', kwargs={'pk': task.project.id})


class ProductionLineSiteView(LoginRequiredMixin, View):
    """Show all of production lines"""

    def get(self, request):
        productionlines = ProductionLine.objects.all().order_by('line_name')
        return render(request, 'productionline_site.html', {'productionlines': productionlines})


class ProductionLineDetailsView(LoginRequiredMixin, View):
    """Show details of chosen production line"""
    login_url = '/login'

    def get(self, request, pk):
        pro_line = ProductionLine.objects.get(pk=pk)
        workers = Employees.objects.filter(production_line__pk=pk).order_by('name')
        return render(request, 'productionline_details.html', {'pro_line': pro_line, 'workers': workers})


class ProductionLineEditView(LoginRequiredMixin, UpdateView):
    """Edit production line"""
    login_url = '/login'

    model = ProductionLine
    fields = '__all__'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        """Move to site with details of checged production line"""

        pro_line = self.object
        return reverse('productionline-details', kwargs={'pk': pro_line.pk})


class ProductionLineDeleteView(LoginRequiredMixin, DeleteView):
    """Delete production line"""
    login_url = '/login'

    model = ProductionLine
    success_url = '/productionlinesite'


class RaportCreateView(LoginRequiredMixin, View):
    """Create new raport"""
    login_url = '/login'

    def get(self, request):
        """Render empty form"""
        form = RaportForm(initial={'date': datetime.now(), 'quantity': 1})
        return render(request, 'raport_create_form.html', {'form': form})

    def post(self, request):
        """Save raport and update data in project task"""
        form = RaportForm(request.POST)
        if form.is_valid():
            production_line = form.cleaned_data.get('production_line')
            time = form.cleaned_data.get('time')
            quantity = form.cleaned_data.get('quantity')
            date = form.cleaned_data.get('date')
            workers = Employees.objects.filter(production_line_id=production_line.pk).order_by('name')
            workerss = ''
            for worker in workers:
                workerss += f'{worker.name} {worker.surname}, '
            workerss = workerss[0:-2]
            task = production_line.work

            raport = Raports.objects.create(production_line=production_line, time=time, quantity=quantity, date=date,
                                            workers=workerss, task=task)
            work = production_line.work
            print(work.done)
            if work.done == 0:
                work.efficiency = (time*60)/quantity
                work.done += quantity
            else:
                work.efficiency = ((work.efficiency*work.done)+(time*60))/(work.done+quantity)
                work.done += quantity
            work.save()

            return redirect('raport-details', pk=raport.pk)
        else:
            return render(request, 'raport_create_form.html', {'form': form})


class RaportSiteView(LoginRequiredMixin, View):
    """Site with all raports"""
    login_url = '/login'

    def get(self, request):
        raports = Raports.objects.all().order_by('-date')
        return render(request, 'raport_site.html', {'raports': raports})


class RaportDetailsView(LoginRequiredMixin, View):
    """Show all details of specific raport"""
    login_url = '/login'

    def get(self, request, pk):
        raport = Raports.objects.get(pk=pk)
        return render(request, 'raport_details.html', {'raport': raport})


class RaportDeleteView(LoginRequiredMixin, DeleteView):
    """Delete raport"""
    login_url = '/login'

    model = Raports
    success_url = '/raportsite'


class CreateProjectRaportPDF(View):

    def get(self, request, pk):
        """Create project raport in .pdf"""

        project = Projects.objects.get(pk=pk)
        tasks = Work.objects.filter(project__pk=pk)
        if tasks:
            sum_progress = 0
            sum_time = 0
            for work in tasks:
                sum_time += (project.quantity - work.done) * work.efficiency
                sum_progress += work.done
            sum_progress = (sum_progress / (project.quantity * tasks.count())) * 100
            sum_progress = round(sum_progress, 2)
            sum_time = round(sum_time / 60, 2)
        else:
            sum_progress = 0
            sum_time = 'Unknown'

        doc = SimpleDocTemplate(f"{project}.pdf", pagesize=A4,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=28)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='center', alignment=TA_CENTER, fontSize=24))
        styles.add(ParagraphStyle(name='task', leftIndent=10))
        styles.add(ParagraphStyle(name='end', alignment=TA_CENTER, fontSize=7, spaceBefore=35))

        cont = []
        text = f"Project nr.{project.project_number} report"
        cont.append(Paragraph(text, styles["center"]))
        cont.append(Spacer(1, 100))

        text = f"<b>Customer:</b> {project.customer}"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(111, 5))
        text = f"<b>Project number:</b> {project.project_number}"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 5))
        text = f"<b>Status:</b> {project.project_status}"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 5))
        text = f"<b>Dead line:</b> {project.dead_line}"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 5))
        text = f"<b>Quantity:</b> {project.quantity}"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 5))
        text = f"<b>Progress:</b> {sum_progress}%"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 5))
        text = f"<b>Estimated hours to complete the project:</b> {sum_time}"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 10))
        text = f"<b>Tasks:</b>"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 5))
        for task in tasks:
            text = f"<b>Tag:</b> {task.shortcut}"
            cont.append(Paragraph(text, styles["task"]))
            cont.append(Spacer(1, 5))
            text = f"<b>Description:</b> {task.description}"
            cont.append(Paragraph(text, styles["task"]))
            cont.append(Spacer(1, 5))
            text = f"<b>Done:</b> {task.done}"
            cont.append(Paragraph(text, styles["task"]))
            cont.append(Spacer(1, 5))
            text = f"<b>Min for piece:</b> {task.efficiency}"
            cont.append(Paragraph(text, styles["task"]))
            cont.append(Spacer(1, 15))
        text = f"Report was generated on {date.today()} by ProjectManager"
        cont.append(Paragraph(text, styles["end"]))
        cont.append(Spacer(1, 10))

        doc.build(cont)

        return render(request, 'project_details.html', {'project': project, 'tasks': tasks, 'progress': sum_progress,
                                                        'sum_time': sum_time})


class CreateProjectRaportXLSX(View):

    def get(self, request, pk):
        """Create project report in xlsx"""

        project = Projects.objects.get(pk=pk)
        tasks = Work.objects.filter(project__pk=pk)
        if tasks:
            sum_progress = 0
            sum_time = 0
            for work in tasks:
                sum_time += (project.quantity - work.done) * work.efficiency
                sum_progress += work.done
            sum_progress = (sum_progress / (project.quantity * tasks.count())) * 100
            sum_progress = round(sum_progress, 2)
            sum_time = round(sum_time / 60, 2)
        else:
            sum_progress = 0
            sum_time = 'Unknown'

        reports = xlsxwriter.Workbook(f'{project}.xlsx')
        report = reports.add_worksheet()
        report.set_column(0, 2, width=15)

        row = 3
        col = 0

        report.write(1, 1, f"Project nr.{project.project_number} report")
        report.write(row, col, 'Customer:')
        report.write(row, col + 1, f'{project.customer}')
        row += 1
        report.write(row, col, 'Project number:')
        report.write(row, col + 1, f'{project.project_number}')
        row += 1
        report.write(row, col, 'Status:')
        report.write(row, col + 1, f'{project.project_status}')
        row += 1
        report.write(row, col, 'Dead line:')
        report.write(row, col + 1, f'{project.dead_line}')
        row += 1
        report.write(row, col, 'Quantity:')
        report.write(row, col + 1, f'{project.quantity}')
        row += 1
        report.write(row, col, 'Progress:')
        report.write(row, col + 1, f'{sum_progress}%')
        row += 1
        report.write(row, col, 'Hours work left:')
        report.write(row, col + 1, f'{sum_time}')
        row += 2
        report.write(row, col, 'Tasks:')
        row += 1
        for task in tasks:
            report.write(row, col + 1, 'Tag:')
            report.write(row, col + 2, f'{task.shortcut}')
            row += 1
            report.write(row, col + 1, 'Description:')
            report.write(row, col + 2, f'{task.description}')
            row += 1
            report.write(row, col + 1, 'Done:')
            report.write(row, col + 2, f'{task.done}')
            row += 1
            report.write(row, col + 1, 'Min for piece:')
            report.write(row, col + 2, f'{task.efficiency}')
            row += 2


        reports.close()

        return render(request, 'project_details.html', {'project': project, 'tasks': tasks, 'progress': sum_progress,
                                                        'sum_time': sum_time})


class LoginView(View):
    """Login user"""

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            if User.objects.filter(username=username):
                user = authenticate(request, username=username, password=password)
                if user is None:
                    return HttpResponse('Uncorrect password')
                else:
                    login(request, user)
                    return redirect('home')
            else:
                return HttpResponse('There is no such user')


@login_required(login_url='/login')
def logout_view(request):
    """Logout user"""

    logout(request)
    return redirect('login')
