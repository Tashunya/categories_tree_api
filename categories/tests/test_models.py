from django.test import TestCase
from django.db import IntegrityError
from ..models import Category


class CategoryTest(TestCase):
    """ Test module for Category module """

    def setUp(self) -> None:
        Category.objects.create(name="Category 1", parent=None)
        Category.objects.create(name="Category 2", parent=None)

    def test_category_obj(self):
        cat_1 = Category.objects.get(name="Category 1")
        self.assertEqual(cat_1.name, "Category 1")

    def test_child_category_obj(self):
        cat_1 = Category.objects.get(name="Category 1")
        cat_2 = Category.objects.get(name="Category 2")
        cat_1_1 = Category.objects.create(name="Category 1.1", parent=cat_1)
        self.assertTrue(cat_1_1.parent_id == cat_1.id)
        self.assertFalse(cat_1_1.parent_id == cat_2.id)

    def test_unique_field(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Category 2", parent=None)

    print("All done")
