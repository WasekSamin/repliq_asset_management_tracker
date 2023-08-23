from .models import (
    Company,
)
from employee.models import (
    Employee,
)
from device.models import (
    DeviceDistribution,
)
from .serializers import (
    CompanySerializer,
)
from device.serializers import (
    DeviceDistributionSerializer,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from device_tracker_core.update_datetime import (
    update_obj_updated_datetime,
)
from drf_yasg.utils import swagger_auto_schema


class CompanyList(APIView):
    # Get all companies
    def get(self, request, format=None):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    # Create new company
    @swagger_auto_schema(request_body=CompanySerializer)
    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CompanyDetail(APIView):
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    # Get single company
    def get(self, request, pk, format=None):
        company_obj = self.get_object(pk)
        serializer = CompanySerializer(company_obj)
        return Response(serializer.data)

    # Update single company
    @swagger_auto_schema(request_body=CompanySerializer)
    def put(self, request, pk, format=None):
        company_obj = self.get_object(pk)

        serializer = CompanySerializer(company_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update the datetime of the object's updated_at
            update_obj_updated_datetime(company_obj)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete single company
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Companies should be able to see when a Device was checked out and returned
class CompanyDeviceCheckView(APIView):
    def get(self, request, company_pk):
        company_obj = Company.get_company_obj_by_pk(self, company_pk)

        if company_obj is None:
            return Response({"msg": "Company not found!"}, status=status.HTTP_404_NOT_FOUND)

        # Getting all the employees of the company
        employees = Employee.objects.filter(company=company_obj)
        # Getting all the devices of each employee for that particular company
        dev_dists = DeviceDistribution.objects.filter(employee__pk__in=[emp.pk for emp in employees])

        serializer = DeviceDistributionSerializer(dev_dists, many=True)
        return Response(serializer.data)