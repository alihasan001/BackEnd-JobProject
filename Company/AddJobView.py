from django.shortcuts import render
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .Serializers import *
from rest_framework import status
import datetime
import xml.etree.ElementTree as ET
from django.db.models import Q
import json


def read_tag(list):
    l = {}
    for i in list:
        if i.text != None:
            l[i.tag] = i.text
        else:
            l[i.tag] = ""
    return l


def read_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    l = []
    for elem in root:
        l.append(read_tag(elem))
    return l


class addJobs(APIView):
    def post(self, request):
        data = request.data['file']
        try:
            data = read_xml(data)
            print(data[0]['AdvertiserName'])
            for i in data:
                datatime = i['PostDate'].split("T")
                datatime[0] = datatime[0].split("-")
                datatime[1] = datatime[1].split(":")
                i['PostDate'] = datetime.datetime(int(datatime[0][0]), int(datatime[0][1]), int(datatime[0][2]),
                                                  int(datatime[1][0]), int(datatime[1][1]), int(datatime[1][2]))
                # print(i['PostDate'])
                if i['StartDate'] == "":
                    i["StartDate"] = None
                company = Company.objects.filter(Name=i['AdvertiserName'])[0]
                if not Company.objects.filter(Name=i['AdvertiserName']).exists():
                    if i['LogoURL'] == "":
                        company = Company(Name=i['AdvertiserName'], Location=i['Location'],
                                          WebSite=i['DescriptionURL'], About=i['AdvertiserType'], Categories=i['Classification']
                                          )
                        company.save()
                    else:
                        company = Company(Name=i['AdvertiserName'], Location=i['Location'],
                                          WebSite=i['DescriptionURL'], About=i['AdvertiserType'], logo=i['LogoURL'], Categories=i['Classification']
                                          )
                        company.save()
                if i['LogoURL'] == "":
                    job = Job(
                        Company=company,
                        AdvertiserName=i['AdvertiserName'],  AdvertiserType=i['AdvertiserType'], SenderReference=i['SenderReference'],
                        DisplayReference=i['DisplayReference'], PostDate=i['PostDate'], Classification=i['Classification'],
                        SubClassification=i['SubClassification'], Position=i['Position'], Description=i['Description'],
                        Country=i['Country'], Location=i['Location'], Area=i['Area'],
                        PostalCode=i['PostalCode'], ApplicationURL=i['ApplicationURL'], DescriptionURL=i['DescriptionURL'],
                        Language=i['Language'],
                        ContactName=i['ContactName'], EmploymentType=i['EmploymentType'], StartDate=i['StartDate'],
                        Duration=i['Duration'], WorkHours=i['WorkHours'], SalaryCurrency=i['SalaryCurrency'],
                        SalaryMinimum=i['SalaryMinimum'], SalaryMaximum=i['SalaryMaximum'], SalaryPeriod=i['SalaryPeriod'],
                        SalaryAdditional=i['SalaryAdditional'], JobSource=i['JobSource'], JobSourceURL=i['JobSourceURL'],
                        VideoLinkURL=i['VideoLinkURL'], AdditionalClassification1=i['AdditionalClassification1'],
                        AdditionalClassification2=i['AdditionalClassification2'], AdditionalClassification3=i['AdditionalClassification3'],
                        AdditionalClassification4=i['AdditionalClassification4'], JobType=i['JobType']
                    )
                    job.save()
                else:
                    job = Job(
                        Company=company,
                        AdvertiserName=i['AdvertiserName'],  AdvertiserType=i['AdvertiserType'], SenderReference=i['SenderReference'],
                        DisplayReference=i['DisplayReference'], PostDate=i['PostDate'], Classification=i['Classification'],
                        SubClassification=i['SubClassification'], Position=i['Position'], Description=i['Description'],
                        Country=i['Country'], Location=i['Location'], Area=i['Area'],
                        PostalCode=i['PostalCode'], ApplicationURL=i['ApplicationURL'], DescriptionURL=i['DescriptionURL'],
                        Language=i['Language'],
                        ContactName=i['ContactName'], EmploymentType=i['EmploymentType'], StartDate=i['StartDate'],
                        Duration=i['Duration'], WorkHours=i['WorkHours'], SalaryCurrency=i['SalaryCurrency'],
                        SalaryMinimum=i['SalaryMinimum'], SalaryMaximum=i['SalaryMaximum'], SalaryPeriod=i['SalaryPeriod'],
                        SalaryAdditional=i['SalaryAdditional'], JobSource=i['JobSource'], JobSourceURL=i['JobSourceURL'],
                        VideoLinkURL=i['VideoLinkURL'], AdditionalClassification1=i['AdditionalClassification1'],
                        AdditionalClassification2=i['AdditionalClassification2'], AdditionalClassification3=i['AdditionalClassification3'],
                        AdditionalClassification4=i['AdditionalClassification4'],
                        LogoURL=i['LogoURL'], JobType=i['JobType']
                    )
                    job.save()
            return Response({'Data': data})
        except:
            message = {'detail': 'Error in File Reading'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class Search(APIView):
    def post(self, request):
        data = request.data
        search = data['search']
        print(search)
        if search != "":
            try:
                lookup = Q(AdvertiserName__icontains=search) | Q(AdvertiserType__icontains=search) | Q(Classification__icontains=search) | Q(
                    Position__icontains=search) | Q(Description__icontains=search) | Q(Country__icontains=search) | Q(Location__icontains=search)
                job = Job.objects.filter(
                    lookup).distinct().order_by('AdvertiserName')
            except:
                message = {'detail': 'Error in File Reading'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            job = Job.objects.all()
        Country = request.data['Country'].split(",")
        category = request.data['category'].split(",")
        companies = request.data['companies'].split(",")
        # print(job)
        # print(Country,category,companies)
        if Country != [""]:
            print(1)
            job = job.filter(Q(Country__in=Country))
        # print((job))
        if companies != [""]:
            print(2)
            job = job.filter(Q(AdvertiserName__in=companies))
        # print((job))
        if category != [""]:
            print(3)
            job = job.filter(Q(Classification__in=category))
        print(len(job))
        job = JobSerializer(job, many=True)
        return Response({'data': job.data})
