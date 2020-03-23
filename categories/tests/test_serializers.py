from django.test import TestCase
from ..serializers import CategorySerializer, \
    CategoryTreeCreateSerializer as CTCSerializer


class CategorySerializerTest(TestCase):
    serializer_class = CategorySerializer

    def setUp(self):
        self.valid_data = {"id": 1, 'name': "Category 1"}
        self.invalid_data = {"id": 3, 'name': ""}

    def test_valid_serializer(self):
        serializer = CategorySerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(serializer.validated_data, self.valid_data)
        self.assertFalse(serializer.errors)

    def test_invalid_serializer(self):
        serializer = CategorySerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertFalse(serializer.validated_data)


class CategoryTreeCreateSerializerTest(TestCase):
    serializer_class = CTCSerializer

    def setUp(self):
        self.valid_structure = {
            "name": "Category 2",
            "children": [
                {
                    "name": "Category 2.1",
                    "children": [
                        {
                            "name": "Category 2.1.1",
                            "children": [
                                {
                                    "name": "Category 2.1.1.1"
                                },
                            ]
                        },
                        {
                            "name": "Category 2.1.2",
                        }
                    ]
                },
            ]
        }

        self.valid_structure_2 = {
            "name": "Category 2"
        }

        self.invalid_structure_1 = {}

        self.invalid_structure_2 = []

        self.invalid_structure_3 = {
            "name": "Category 2",
            "children": [
                {
                    "name": "",
                },
            ]
        }

        self.invalid_structure_4 = {
            "name": "Category 2",
            "children": [
                {
                    "name": "Category 2.1",
                    "child": [
                        {
                            "name": "Category 2.1.1",
                        },
                    ]
                },
            ]
        }

        self.invalid_structure_5 = {
            "name": "Category 2",
            "children": [
                {
                    "name": 12,
                }
            ]
        }

        self.invalid_structure_6 = {
            "name": "Category 2",
            "children": [
                {
                    "children": [
                        {
                            "name": "Category 2.1.1",
                        }
                    ]
                }
            ]
        }

    def test_check_valid_structure(self):
        self.assertTrue(
            CTCSerializer.check_structure(self.valid_structure))

    def test_no_children(self):
        self.assertTrue(
            CTCSerializer.check_structure(self.valid_structure_2)
        )

    def test_check_empty_structure(self):
        self.assertFalse(
            CTCSerializer.check_structure(self.invalid_structure_1))

    def test_check_list_structure(self):
        self.assertFalse(
            CTCSerializer.check_structure(self.invalid_structure_2))

    def test_check_empty_name(self):
        self.assertFalse(
            CTCSerializer.check_structure(self.invalid_structure_3))

    def test_check_invalid_key(self):
        self.assertFalse(
            CTCSerializer.check_structure(self.invalid_structure_4))

    def test_check_invalid_value(self):
        self.assertFalse(
            CTCSerializer.check_structure(self.invalid_structure_5))

    def test_check_no_key(self):
        self.assertFalse(
            CTCSerializer.check_structure(self.invalid_structure_6))
