from django.urls import path
from . import views
urlpatterns = [
    path('getID/<int:id>',views.getId.as_view()), #get company by Id
    path('getName/<str:Name>',views.getName.as_view()), #get company by name
    path('getAllCompany',views.getAll.as_view()), #get all comapnies data
    path('addNewCompany',views.addNewCompany.as_view()), #add new company Post request
    path('addJobs',views.addJobs.as_view()), #add a new Job
    path('getAllCategories',views.getAllCategories.as_view()), #get all categories
    path('getAllCountries',views.getAllCountries.as_view()), #get all available countries with job
    path('getAllCompanies',views.getAllCompanies.as_view()), #get all available Companies with job
    path('Country/<str:Name>',views.getjobCountry.as_view()), #get jobs for specicfic country
    path('JobName/<str:Name>',views.getJobsName.as_view()), #get jobs for specicfic company Name
    path('Category/<str:Name>',views.getJobsCategory.as_view()), #get jobs for specicfic Category
]