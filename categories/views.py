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
        category = get_object_or_404(Category, pk=pk)
        category_serializer = CategoryTreeSerializer(category)
        return Response(category_serializer.data)


class CreateCategory(APIView):
    """
    Create new category tree in db
    """

    def post(self, request):
        tree_data = JSONParser().parse(request)

        if CtgTreeCreate.check_structure(tree_data):
            try:
                CtgTreeCreate.save_structure(tree_data)
            except ValidationError as e:
                return JsonResponse({'detail': e.detail[0]},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                # category_tree_serializer = CategoryTreeSerializer(new_root)
                return JsonResponse({'detail': 'Created'},
                                    status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({'detail': 'Incorrect Category Tree Data'},
                                status=status.HTTP_400_BAD_REQUEST)


