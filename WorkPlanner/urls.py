from django.contrib import admin
from django.urls import path
from plan_app.views import HomeView, ProjectCreateView, WorkCreateView, EmployeeCreateView, ProductionLineCreateView, \
    ProjectSiteView, ProjectEditView, ProjectDeleteView, ProjectDetailsView, WorkEditView, WorkDeleteView, \
    EmployeeSiteView, EmployeeEditView, EmployeeDeleteView, ProductionLineSiteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('createproject', ProjectCreateView.as_view(), name='create-project'),
    path('createemployee', EmployeeCreateView.as_view(), name='create-employee'),
    path('creatework', WorkCreateView.as_view(), name='create-work'),
    path('createproductionline', ProductionLineCreateView.as_view(), name='create-productionline'),
    path('deleteproject/<int:pk>', ProjectDeleteView.as_view(), name='delete-project'),
    path('editproject/<int:pk>', ProjectEditView.as_view(), name='edit-project'),
    path('projectsite', ProjectSiteView.as_view(), name='project-site'),
    path('productionlinesite', ProductionLineSiteView.as_view(), name='productionline-site'),
    path('employeesite', EmployeeSiteView.as_view(), name='employee-site'),
    path('projectdetails/<int:pk>', ProjectDetailsView.as_view(), name='project-details'),
    path('deleteemployee/<int:pk>', EmployeeDeleteView.as_view(), name='delete-employee'),
    path('deletework/<int:pk>', WorkDeleteView.as_view(), name='delete-work'),
    path('editwork/<int:pk>', WorkEditView.as_view(), name='edit-work'),
    path('editemployee/<int:pk>', EmployeeEditView.as_view(), name='edit-employee'),
    path('deleteproductionline', ProductionLineCreateView.as_view(), name='delete-productionline'),
]
