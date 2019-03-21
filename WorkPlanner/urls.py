from django.contrib import admin
from django.urls import path
from plan_app.views import HomeView, ProjectCreateView, WorkCreateView, EmployeeCreateView, ProductionLineCreateView, \
    ProjectSiteView, ProjectEditView, ProjectDeleteView, ProjectDetailsView, WorkEditView, WorkDeleteView, \
    EmployeeSiteView, EmployeeEditView, EmployeeDeleteView, ProductionLineSiteView, ProductionLineDetailsView, \
    ProductionLineEditView, ProductionLineDeleteView, RaportCreateView, RaportSiteView, RaportDetailsView, LoginView, \
    logout_view, RaportDeleteView, CreateProjectRaportPDF, CreateProjectRaportXLSX

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('createproject', ProjectCreateView.as_view(), name='create-project'),
    path('createemployee', EmployeeCreateView.as_view(), name='create-employee'),
    path('creatework', WorkCreateView.as_view(), name='create-work'),
    path('createraport', RaportCreateView.as_view(), name='create-raport'),
    path('raportsite', RaportSiteView.as_view(), name='raport-site'),
    path('createproductionline', ProductionLineCreateView.as_view(), name='create-productionline'),
    path('deleteproject/<int:pk>', ProjectDeleteView.as_view(), name='delete-project'),
    path('editproject/<int:pk>', ProjectEditView.as_view(), name='edit-project'),
    path('projectsite', ProjectSiteView.as_view(), name='project-site'),
    path('productionlinesite', ProductionLineSiteView.as_view(), name='productionline-site'),
    path('employeesite', EmployeeSiteView.as_view(), name='employee-site'),
    path('projectdetails/<int:pk>', ProjectDetailsView.as_view(), name='project-details'),
    path('productionlinedetails/<int:pk>', ProductionLineDetailsView.as_view(), name='productionline-details'),
    path('deleteemployee/<int:pk>', EmployeeDeleteView.as_view(), name='delete-employee'),
    path('deletework/<int:pk>', WorkDeleteView.as_view(), name='delete-work'),
    path('editwork/<int:pk>', WorkEditView.as_view(), name='edit-work'),
    path('editproductionlinek/<int:pk>', ProductionLineEditView.as_view(), name='edit-productionline'),
    path('editemployee/<int:pk>', EmployeeEditView.as_view(), name='edit-employee'),
    path('deleteproductionline/<int:pk>', ProductionLineDeleteView.as_view(), name='delete-productionline'),
    path('raportdetails/<int:pk>', RaportDetailsView.as_view(), name='raport-details'),
    path('raportdelete/<int:pk>', RaportDeleteView.as_view(), name='delete-raport'),
    path('projectraportpdf/<int:pk>', CreateProjectRaportPDF.as_view(), name='project-raport-pdf'),
    path('projectraportxlsx/<int:pk>', CreateProjectRaportXLSX.as_view(), name='project-raport-xlsx'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', logout_view, name='logout'),
]
