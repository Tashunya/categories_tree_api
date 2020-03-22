from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryCreateSerializer(serializers.ModelSerializer):
    # parent = serializers.IntegerField(allow_null=True)
    class Meta:
        model = Category
        fields = ('name', 'parent')

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class CategoryTreeSerializer(serializers.ModelSerializer):
    parents = serializers.SerializerMethodField()
    children = CategorySerializer(many=True, read_only=True)
    siblings = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parents', 'children', 'siblings')

    def get_parents(self, obj):
        # queryset = Category.objects.filter(id=obj.parent_id)
        # return CategorySerializer(queryset, many=True, allow_empty=True).data
        return self.get_parent_lst(obj)

    def get_parent_lst(self, obj):
        if obj.parent_id == None:
            return []
        parent = Category.objects.get(id=obj.parent_id)
        parents_array = [{'id': parent.id, 'name': parent.name}]
        parents_array.extend(self.get_parent_lst(parent))
        return parents_array

    def get_siblings(self, obj):
        queryset = Category.objects.filter(parent_id=obj.parent_id).\
            exclude(id=obj.id)
        return CategorySerializer(queryset, many=True).data


class CategoryTreeCreateSerializer(serializers.ModelSerializer):

    @staticmethod
    def save_children(root_id: int, children: list):
        """
        Create new structure of category tree and save it to database
        :param root_id: id of parent category
        :param children: list of children dicts
        :return: None or Exception
        """
        if len(children) == 0:
            return
        for category in children:
            data = {'name': category['name'], 'parent': root_id}
            child_serializer = CategoryCreateSerializer(data=data)
            # save subcategory in db

            try:
                e = child_serializer.is_valid(raise_exception=True)
            except ValidationError:
                raise serializers.ValidationError(
                    "Category name '{}' is not unique.".\
                        format(category["name"]))

            if e:
                child = child_serializer.save()
                if category.get("children"):
                    CategoryTreeCreateSerializer.\
                        save_children(child.pk, category["children"])

    @staticmethod
    def check_structure(data: dict) -> bool:
        valid_keys = ['name', 'children']
        if not data:
            return False

        for key in data.keys():
            if key not in valid_keys:
                return False

        name_value = data.get('name', '')
        if not isinstance(name_value, str) or not name_value.strip():
            return False

        children = data.get('children', [])
        if not isinstance(children, list):
            return False
        for child in children:
            if not CategoryTreeCreateSerializer.check_structure(child):
                return False
        return True

    class Meta:
        model = Category
        fields = "__all__"
