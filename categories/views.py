""" Views module"""

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from categories.models import Category
from categories.serializers import CategoryTreeSerializer
from categories.serializers import CategoryTreeCreateSerializer as \
    CtgTreeCreate


class CategoryTreeDetail(APIView):
    """
    Retrieve category instance with parents, children and siblings
    Update and delete methods are not allowed
    """

    def get(self, request, pk):
        """
        Return response with status code 200 and category structure in body if
        'pk'
        is valid otherwise response with error 404 and detail in body
        :param request:
        :param pk: category id (int)
        :return: response 200 or 404
        """
        category = get_object_or_404(Category, pk=pk)
        category_serializer = CategoryTreeSerializer(category)
        return Response(category_serializer.data)


class CreateCategoryTree(APIView):
    """ Create new category tree in db """

    def post(self, request):
        """
        Save new or updated category tree to db and return response with
        status code 201 and detail in body if request is valid
        otherwise response with status code 400 and detail in body
        :param request:
        :return:
        """
        tree_data = JSONParser().parse(request)

        if CtgTreeCreate.check_structure(tree_data):
            try:
                CtgTreeCreate.save_structure(tree_data)
            except ValidationError as err:
                return JsonResponse({'detail': err.detail[0]},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'detail': 'Category tree created.'},
                                    status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({'detail': 'Incorrect Category Tree Data'},
                                status=status.HTTP_400_BAD_REQUEST)
