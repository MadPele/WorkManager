from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Projects, Work, Employees, Raports, WorkerProductivity, Expenses
from .forms import RaportForm, LoginForm, ExpenseForm
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
    fields = ['customer', 'project_number', 'dead_line', 'quantity', 'project_status']

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
    fields = ['shortcut', 'description', 'efficiency', 'project']

    def get_success_url(self):

        task = self.object
        return reverse('project-details', kwargs={'pk': task.project.id})


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

        wp = WorkerProductivity.objects.filter(task__project__id=project.id)

        if tasks:
            sum_progress = 0
            sum_time = 0
            for work in tasks:
                sum_time += (project.quantity-work.done)*work.efficiency
                if work.done > project.quantity:
                    sum_progress += project.quantity
                else:
                    sum_progress += work.done
            sum_progress = (sum_progress/(project.quantity*tasks.count()))*100
            sum_progress = round(sum_progress, 2)
            sum_time = round(sum_time/60, 2)
        else:
            sum_progress = 0
            sum_time = 'Unknown'

        now = date.today()
        dead_line = project.dead_line
        delta_days = (dead_line-now).days
        alert_color = ''

        if delta_days > 14 and sum_progress < 100:
            alert_color = 'green'
        elif delta_days <= 14 and delta_days > 7 and sum_progress < 100:
            alert_color = 'orange'
        elif delta_days <= 7 and sum_progress < 100:
            alert_color = 'red'
        else:
            alert_color = 'black'
        if project.project_status != 'In progress':
            alert_color = 'black'

        return render(request, 'project_details.html', {'project': project, 'tasks': tasks, 'progress': sum_progress,
                                            'sum_time': sum_time, 'alert_color': alert_color, 'wp': wp})


class ProjectDailyReports(View):
    """Show all daily reports for project"""

    def get(self, request, pk):
        project = Projects.objects.get(pk=pk)
        reports = Raports.objects.filter(task__project__pk=pk).order_by('-date')
        return render(request, 'project_daily_reports.html', {'reports': reports, 'project': project})


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
    fields = ['shortcut', 'description', 'done', 'project']
    template_name_suffix = '_update_form'

    def get_success_url(self):

        task = self.object
        return reverse('project-details', kwargs={'pk': task.project.id})


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
            time = form.cleaned_data.get('time')
            quantity = form.cleaned_data.get('quantity')
            date = form.cleaned_data.get('date')
            worker = form.cleaned_data.get('worker')
            task = form.cleaned_data.get('task')

            raport = Raports.objects.create(time=time, quantity=quantity, date=date,
                                            worker=worker, task=task)

            project = Projects.objects.get(pk=task.project.pk)
            project.cost += (time*worker.salary)
            project.save()


            if task.done == 0:
                task.efficiency = round((time*60)/quantity, 2)
                task.done += quantity
            else:
                task.efficiency = round(((task.efficiency*task.done)+(time*60))/(task.done+quantity), 2)
                task.done += quantity
            task.save()

            filterargs = {'task': task, 'worker': worker}
            if WorkerProductivity.objects.filter(**filterargs):
                worker_prod = WorkerProductivity.objects.get(**filterargs)
                worker_prod.time = worker_prod.time + time
                worker_prod.quantity += quantity
                worker_prod.average_productivity = worker_prod.quantity/worker_prod.time
                worker_prod.save()
                print(worker_prod.quantity/worker_prod.time)
            else:
                average_productivity = quantity / time
                WorkerProductivity.objects.create(worker=worker, time=time, quantity=quantity, task=task,
                                                       average_productivity=average_productivity)

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


class CreateProjectRaportPDF(LoginRequiredMixin, View):
    """Create project raport in pdf"""
    login_url = '/login'

    def get(self, request, pk):

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
        cont.append(Spacer(1, 5))
        text = f"<b>Current project cost:</b> {project.cost}zl"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 10))
        text = f"<b>Tasks:</b>"
        cont.append(Paragraph(text, styles["Normal"]))
        cont.append(Spacer(1, 5))
        if tasks:
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
        else:
            text = "Here is no any task yet"
            cont.append(Paragraph(text, styles["task"]))
            cont.append(Spacer(1, 15))
        text = f"Report was generated on {date.today()} by Project Manager"
        cont.append(Paragraph(text, styles["end"]))
        cont.append(Spacer(1, 10))

        doc.build(cont)

        return redirect('project-details', pk=project.pk)


class CreateProjectRaportXLSX(LoginRequiredMixin, View):
    """Create project report in xlsx"""
    login_url = '/login'

    def get(self, request, pk):

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
        bold = reports.add_format({'bold': True})
        big_size = reports.add_format({'bold': True, 'font_size': 15, 'align': 'center', 'valign': 'vcenter'})
        report.merge_range(0, 1, 1, 2, f"Project nr.{project.project_number}", big_size)


        row = 4
        col = 0

        report.write(row, col, 'Customer:', bold)
        report.write(row, col + 1, f'{project.customer}')
        row += 1
        report.write(row, col, 'Project number:', bold)
        report.write(row, col + 1, f'{project.project_number}')
        row += 1
        report.write(row, col, 'Status:', bold)
        report.write(row, col + 1, f'{project.project_status}')
        row += 1
        report.write(row, col, 'Dead line:', bold)
        report.write(row, col + 1, f'{project.dead_line}')
        row += 1
        report.write(row, col, 'Quantity:', bold)
        report.write(row, col + 1, f'{project.quantity}')
        row += 1
        report.write(row, col, 'Progress:', bold)
        report.write(row, col + 1, f'{sum_progress}%')
        row += 1
        report.write(row, col, 'Hours work left:', bold)
        report.write(row, col + 1, f'{sum_time}')
        row += 1
        report.write(row, col, 'Project cost:', bold)
        report.write(row, col + 1, f'{project.cost}zł')
        row += 2
        report.write(row, col, 'Tasks:', bold)
        row += 1
        if tasks:
            for task in tasks:
                report.write(row, col + 1, 'Tag:', bold)
                report.write(row, col + 2, f'{task.shortcut}')
                row += 1
                report.write(row, col + 1, 'Description:', bold)
                report.write(row, col + 2, f'{task.description}')
                row += 1
                report.write(row, col + 1, 'Done:', bold)
                report.write(row, col + 2, f'{task.done}')
                row += 1
                report.write(row, col + 1, 'Min for piece:', bold)
                report.write(row, col + 2, f'{task.efficiency}')
                row += 2
        else:
            report.merge_range(14, 1, 14, 2, 'Here is no any task yet')
            row += 3

        low_size = reports.add_format({'font_size': 8, 'align': 'center'})
        report.merge_range(row + 1, 0, row + 1, 2, f"Report was generated on {date.today()} by Project Manager", low_size)

        reports.close()

        return redirect('project-details', pk=project.pk)


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


class CreateExpenseView(LoginRequiredMixin, View):
    """Add expense to project"""
    login_url = '/login'

    def get(self, request, project_pk):
        project = Projects.objects.get(pk=project_pk)
        form = ExpenseForm()
        return render(request, 'create_expense.html', {'form': form, 'project': project})

    def post(self, request, project_pk):
        project = Projects.objects.get(pk=project_pk)
        form = ExpenseForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get('description')
            quantity = form.cleaned_data.get('quantity')
            price = form.cleaned_data.get('price')
            Expenses.objects.create(description=description, quantity=quantity, price=price, project=project)
            project.cost += (quantity*price)
            project.save()
            return redirect('project-details', pk=project_pk)
        else:
            return render(request, 'create_expense.html', {'form': form})


class ShowProjectExpensesView(LoginRequiredMixin, View):
    """Show all expenses for chosen project"""
    login_url = '/login'

    def get(self, request, project_pk):
        project = Projects.objects.get(pk=project_pk)
        expenses = Expenses.objects.filter(project__pk=project_pk)
        return render(request, 'show_project_expenses.html', {'expenses': expenses, 'project': project})

