from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from categories.models import Category
from categories.serializers import CategoryTreeSerializer, \
    CategoryCreateSerializer
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
    Create new category tree
    """

    def post(self, request):
        tree_data = JSONParser().parse(request)

        if CtgTreeCreate.check_structure(tree_data):
            try:
                save_structure(tree_data)
            except ValidationError as e:
                return JsonResponse({'error': e.detail},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                # category_tree_serializer = CategoryTreeSerializer(new_root)
                return JsonResponse({'created': True},
                                    status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({'error': ['Incorrect Category Tree '
                                          'Structure']},
                                status=status.HTTP_400_BAD_REQUEST)


def save_structure(tree_data):
    new_root = None

    try:
        r_ctg_name = tree_data["name"]
        root_category = Category.objects.get(name=r_ctg_name,
                                             parent=None)
        new_root = root_category
    except Category.DoesNotExist:
        new_root = None

    with transaction.atomic():
        if new_root is not None:
            root_category.delete()

        new_root = create_root(tree_data['name'])

        # save the tree in db with serializer
        children = tree_data.get("children", [])
        CtgTreeCreate.save_children(new_root.pk, children)


def create_root(name):
    root_serializer = CategoryCreateSerializer(data={'name': name,
                                                     'parent': None})

    if root_serializer.is_valid(raise_exception=True):
        root = root_serializer.create({'name': name,
                                       'parent': None})
        return root
