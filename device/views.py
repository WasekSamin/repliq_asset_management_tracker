from .models import (
    Category, Device, DeviceDistribution
)
from .serializers import (
    CategorySerializer, DeviceSerializer, DeviceDistributionSerializer
)
from employee.models import (
    Employee,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from device_tracker_core.update_datetime import (
    update_obj_updated_datetime,
)
from drf_yasg.utils import swagger_auto_schema


class CategoryList(APIView):
    # Get all categories
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # Create new category
    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    # Get single category
    def get(self, request, pk, format=None):
        cat_obj = self.get_object(pk)
        serializer = CategorySerializer(cat_obj)
        return Response(serializer.data)

    # Update single category
    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk, format=None):
        cat_obj = self.get_object(pk)
        serializer = CategorySerializer(cat_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Update the datetime of the object's updated_at
            update_obj_updated_datetime(cat_obj)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete single category
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DeviceList(APIView):
    # Get all devices
    def get(self, request, format=None):
        devices = Device.objects.all()
        serializer = DeviceSerializer(devices, many=True)
        return Response(serializer.data)

    # Create new device
    @swagger_auto_schema(request_body=DeviceSerializer)
    def post(self, request, format=None):
        # Get device category pk
        category_pk = request.data.get("device_category")
        category_obj = None

        if category_pk is not None:
            category_obj = Category.get_category_obj_by_pk(self, category_pk)

            # If category object not found, then return an error response
            if category_obj is None:
                return Response({"msg": "Category not found!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(device_category=category_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeviceDetail(APIView):
    def get_object(self, pk):
        try:
            return Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            raise Http404

    # Get single device
    def get(self, request, pk, format=None):
        device_obj = self.get_object(pk)
        serializer = DeviceSerializer(device_obj)
        return Response(serializer.data)

    # Update single device
    @swagger_auto_schema(request_body=DeviceSerializer)
    def put(self, request, pk, format=None):
        device_obj = self.get_object(pk)

        category_pk = request.data.get("device_category")
        category_obj = device_obj.device_category

        if category_pk is not None:
            category_obj = Category.get_category_obj_by_pk(self, category_pk)

            if category_obj is None:
                return Response({"msg": "Category not found!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceSerializer(device_obj, data=request.data)
        if serializer.is_valid():
            serializer.save(device_category=category_obj)

            # Update the datetime of the object's updated_at
            update_obj_updated_datetime(device_obj)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete single device
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class DeviceDistributionList(APIView):
    # Get all device distibutions
    def get(self, request, format=None):
        div_dists = DeviceDistribution.objects.all()
        serializer = DeviceDistributionSerializer(div_dists, many=True)
        return Response(serializer.data)

    # Create new device distibution
    @swagger_auto_schema(request_body=DeviceDistributionSerializer)
    def post(self, request, format=None):
        employee_pk = request.data.get("employee")
        device_pks = request.data.get("devices")

        # Check if employee is provided
        if employee_pk is None:
            return Response({"msg": "Employee is required!"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get employee object from the employee pk
        emp_obj = Employee.get_employee_obj_by_pk(self, employee_pk)

        # If employee object not found, then return an error response
        if emp_obj is None:
            return Response({"msg": "Employee not found!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceDistributionSerializer(data=request.data)
        if serializer.is_valid():
            dev_dist_obj = serializer.save(employee=emp_obj)

            if device_pks is not None and isinstance(device_pks, list):
                # Adding devices to the DeviceDistribution object
                for device_pk in device_pks:
                    device_obj = Device.get_device_obj_by_pk(self, device_pk)

                    if device_obj is None:
                        continue
                    dev_dist_obj.devices.add(device_obj.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeviceDistributionDetail(APIView):
    def get_object(self, pk):
        try:
            return DeviceDistribution.objects.get(pk=pk)
        except DeviceDistribution.DoesNotExist:
            raise Http404

    # Get single device distribution
    def get(self, request, pk, format=None):
        dev_dist_obj = self.get_object(pk)
        serializer = DeviceDistributionSerializer(dev_dist_obj)
        return Response(serializer.data)

    # Update single device distribution
    @swagger_auto_schema(request_body=DeviceDistributionSerializer)
    def put(self, request, pk, format=None):
        dev_dist_obj = self.get_object(pk)

        emp_pk = request.data.get("employee")
        device_pks = request.data.get("devices")

        emp_obj = dev_dist_obj.employee

        if emp_pk is not None:
            emp_obj = Employee.get_employee_obj_by_pk(self, emp_pk)

            # If employee object not found, then return an error response
            if emp_obj is None:
                return Response({"msg": "Employee not found!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = DeviceDistributionSerializer(dev_dist_obj, data=request.data)
        if serializer.is_valid():
            dev_dist_obj = serializer.save(employee=emp_obj)

            if device_pks is not None and isinstance(device_pks, list):
                # Adding devices to the DeviceDistribution object
                for device_pk in device_pks:
                    device_obj = Device.get_device_obj_by_pk(self, device_pk)

                    if device_obj is None:
                        continue
                    dev_dist_obj.devices.add(device_obj.id)

            # Update the datetime of the object's updated_at
            update_obj_updated_datetime(dev_dist_obj)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete single device distribution
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)