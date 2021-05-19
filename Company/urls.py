from django.urls import path
from . import views
from . import AddJobView
urlpatterns = [
    path('getID/<int:id>', views.getId.as_view()),  # get company by Id
    path('getName/<str:Name>', views.getName.as_view()),  # get company by name
    path('getAllCompany', views.getAll.as_view()),  # get all comapnies data
    # add new company Post request
    path('addNewCompany', views.addNewCompany.as_view()),
    path('addJobs', AddJobView.addJobs.as_view()),  # add a new Job
    # get all categories
    path('getAllCategories', views.getAllCategories.as_view()),
    # get all available countries with job
    path('getAllCountries', views.getAllCountries.as_view()),
    path('getCountry', AddJobView.Search.as_view()),
    # get all available Companies with job
    path('getAllCompanies', views.getAllCompanies.as_view()),
    # get jobs for specicfic country
    path('Country/<str:Country>', views.getjobCountry.as_view()),
    # get jobs for specicfic company Name
    path('JobName/<str:JobName>', views.getJobsName.as_view()),
    # get jobs for specicfic Category
    path('Category/<str:Category>', views.getJobsCategory.as_view()),
]
