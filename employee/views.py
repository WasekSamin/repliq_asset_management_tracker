from .models import (
    Role, Employee
)
from .serializers import (
    RoleSerializer, EmployeeSerializer,
)
from company.models import (
    Company,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from device_tracker_core.update_datetime import (
    update_obj_updated_datetime,
)
from drf_yasg.utils import swagger_auto_schema


class RoleList(APIView):
    # Get all roles
    def get(self, request, format=None):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    # Create new role
    @swagger_auto_schema(request_body=RoleSerializer)
    def post(self, request, format=None):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RoleDetail(APIView):
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            raise Http404

    # Get single role
    def get(self, request, pk, format=None):
        role_obj = self.get_object(pk)
        serializer = RoleSerializer(role_obj)
        return Response(serializer.data)

    # Update single role
    @swagger_auto_schema(request_body=RoleSerializer)
    def put(self, request, pk, format=None):
        role_obj = self.get_object(pk)
        serializer = RoleSerializer(role_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update the datetime of the object's updated_at
            update_obj_updated_datetime(role_obj)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete single role
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class EmployeeList(APIView):
    # Get all employees
    def get(self, request, format=None):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    # Create new employee
    @swagger_auto_schema(request_body=EmployeeSerializer)
    def post(self, request, format=None):
        company_pk = request.data.get("company")
        role_pk = request.data.get("role")

        # Check if company is provided
        if company_pk is None:
            return Response({"msg": "Company is required!"}, status=status.HTTP_400_BAD_REQUEST)
        # Check if role is provided
        if role_pk is None:
            return Response({"msg": "Role is required!"}, status=status.HTTP_400_BAD_REQUEST)

        # Get company object from the company pk
        company_obj = Company.get_company_obj_by_pk(self, company_pk)
        # Get role object from the role pk
        role_obj = Role.get_role_obj_by_pk(self, role_pk)

        # If company object not found, then return an error response
        if company_obj is None:
            return Response({"msg": "Company not found!"}, status=status.HTTP_400_BAD_REQUEST)
        # If role object not found, then return an error response
        if role_obj is None:
            return Response({"msg": "Role not found!"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company_obj, role=role_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    # Get single employee
    def get(self, request, pk, format=None):
        emp_obj = self.get_object(pk)
        serializer = EmployeeSerializer(emp_obj)
        return Response(serializer.data)

    # Update single employee
    @swagger_auto_schema(request_body=EmployeeSerializer)
    def put(self, request, pk, format=None):
        emp_obj = self.get_object(pk)

        # Get company pk and role pk
        company_pk = request.data.get("company")
        role_pk = request.data.get("role")

        serializer = EmployeeSerializer(emp_obj, data=request.data)
        if serializer.is_valid():
            company_obj = emp_obj.company
            role_obj = emp_obj.role

            if company_pk is not None:
                company_obj = Company.get_company_obj_by_pk(self, company_pk)

                # If company object not found, then return an error response
                if company_obj is None:
                    return Response({"msg": "Company not found!"}, status=status.HTTP_400_BAD_REQUEST)
            if role_pk is not None:
                role_obj = Role.get_role_obj_by_pk(self, role_pk)

                # If role object not found, then return an error response
                if role_obj is None:
                    return Response({"msg": "Role not found!"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(company=company_obj, role=role_obj)

            # Update the datetime of the object's updated_at
            update_obj_updated_datetime(emp_obj)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete single employee
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)