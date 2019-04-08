from django.contrib import admin
from django.urls import path
from plan_app.views import HomeView, ProjectCreateView, WorkCreateView, EmployeeCreateView,  \
    ProjectSiteView, ProjectEditView, ProjectDeleteView, ProjectDetailsView, WorkEditView, WorkDeleteView, \
    EmployeeSiteView, EmployeeEditView, EmployeeDeleteView, CreateExpenseView, \
    RaportCreateView, RaportSiteView, RaportDetailsView, LoginView, ShowProjectExpensesView, \
    logout_view, RaportDeleteView, CreateProjectRaportPDF, CreateProjectRaportXLSX, ProjectDailyReports

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('createproject', ProjectCreateView.as_view(), name='create-project'),
    path('createemployee', EmployeeCreateView.as_view(), name='create-employee'),
    path('creatework', WorkCreateView.as_view(), name='create-work'),
    path('createraport', RaportCreateView.as_view(), name='create-raport'),
    path('createexpense/<int:project_pk>', CreateExpenseView.as_view(), name='create-expense'),
    path('raportsite', RaportSiteView.as_view(), name='raport-site'),
    path('deleteproject/<int:pk>', ProjectDeleteView.as_view(), name='delete-project'),
    path('editproject/<int:pk>', ProjectEditView.as_view(), name='edit-project'),
    path('projectsite', ProjectSiteView.as_view(), name='project-site'),
    path('projectexpenses/<int:project_pk>', ShowProjectExpensesView.as_view(), name='project-expenses'),
    path('employeesite', EmployeeSiteView.as_view(), name='employee-site'),
    path('projectdetails/<int:pk>', ProjectDetailsView.as_view(), name='project-details'),
    path('deleteemployee/<int:pk>', EmployeeDeleteView.as_view(), name='delete-employee'),
    path('deletework/<int:pk>', WorkDeleteView.as_view(), name='delete-work'),
    path('editwork/<int:pk>', WorkEditView.as_view(), name='edit-work'),
    path('editemployee/<int:pk>', EmployeeEditView.as_view(), name='edit-employee'),
    path('raportdetails/<int:pk>', RaportDetailsView.as_view(), name='raport-details'),
    path('raportdelete/<int:report_pk>', RaportDeleteView.as_view(), name='delete-raport'),
    path('projectraportpdf/<int:pk>', CreateProjectRaportPDF.as_view(), name='project-raport-pdf'),
    path('projectraportxlsx/<int:pk>', CreateProjectRaportXLSX.as_view(), name='project-raport-xlsx'),
    path('projectdailyreports/<int:pk>', ProjectDailyReports.as_view(), name='project-daily-raports'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
]
