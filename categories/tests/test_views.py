""" Test module for views """

import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Category


client = Client()


class GetCategoryTreeTest(TestCase):
    """ Test module for CategoryTreeDetail APIView"""

    def setUp(self):
        cat_1 = Category.objects.create(name="Category 1",
                                        parent=None)
        cat_1_1 = Category.objects.create(name="Category 1.1",
                                          parent=cat_1)
        Category.objects.create(name="Category 1.2", parent=cat_1_1)
        Category.objects.create(name="Category 1.3", parent=cat_1_1)

        self.correct_response = {'id': 1,
                                 'name': 'Category 1',
                                 'parents': [],
                                 'children': [
                                     {'id': 2,
                                      'name': 'Category 1.1'}
                                 ],
                                 'siblings': []}

    def test_get_category_by_id(self):
        """ Requests with valid id should return 200 status"""
        cat = Category.objects.get(name="Category 1")
        response = client.get(reverse('category_tree',
                                      kwargs={'pk': cat.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         "Incorrect status code")
        self.assertEqual(response.data, self.correct_response)
        self.assertEqual(len(response.data), 5)

    def test_get_category_invalid_id(self):
        """ Requests with invalid id should return 404 error """
        invalid_id = 300
        response = client.get(reverse('category_tree',
                                      kwargs={'pk': invalid_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_request_not_allowed_methods(self):
        """ Sending requests by post method should return 405 error """
        cat = Category.objects.get(name="Category 1")
        response = client.post(reverse('category_tree',
                                       kwargs={'pk': cat.id}))
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED,
                         "Incorrect status code")


class CreateCategoryTreeTest(TestCase):
    """ Test module for CreateCategoryTree APIView"""

    def setUp(self):
        self.valid_payload = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                        },
                        {
                            "name": "Category 1.1.2",
                            "children": [
                                {
                                    "name": "Category 1.1.2.1"
                                },

                            ]
                        }
                    ]
                },
                {
                    "name": "Category 1.2",
                    "children": [
                        {
                            "name": "Category 1.2.1"
                        },
                        {
                            "name": "Category 1.2.2",
                            "children": [
                                {
                                    "name": "Category 1.2.2.1"
                                },
                                {
                                    "name": "Category 1.2.2.2"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.empty_payload = {}

        # empty string for key "name"
        self.invalid_payload = {
            "name": "Category 2",
            "children": [
                {
                    "name": "",
                    "children": [
                        {
                            "name": "Category 2.1.1",
                            "children": [
                                {
                                    "name": "Category 2.1.1.1"
                                },
                                {
                                    "name": "Category 2.1.1.2"
                                },
                                {
                                    "name": "Category 2.1.1.3"
                                }
                            ]
                        },

                    ]
                },
            ]
        }

        # repeated name "Category 1.1.1"
        self.duplicate_payload = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1",
                        },
                        {
                            "name": "Category 1.1.1",
                            "children": [
                                {
                                    "name": "Category 1.1.2.1"
                                },

                            ]
                        }
                    ]
                },
            ]
        }

    def test_create_valid_category_tree(self):
        """ Correct requests should return 201 status"""
        response = client.post(
            reverse('create_category_tree'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_body["detail"], "Category tree created.")

    def test_create_invalid_category_tree(self):
        """
        Requests with incorrect data structure or empty data should
        return 400 error and message with details
        """
        response = client.post(
            reverse('create_category_tree'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_body["detail"], "Incorrect Category Tree "
                                                  "Data")

        response = client.post(
            reverse('create_category_tree'),
            data=json.dumps(self.empty_payload),
            content_type='application/json'
        )
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_body["detail"], "Incorrect Category Tree "
                                                  "Data")

    def test_create_duplicate_category(self):
        """
        Requests with duplicated category name should return
        404 error and message with details
        """
        response = client.post(
            reverse('create_category_tree'),
            data=json.dumps(self.duplicate_payload),
            content_type='application/json'
        )
        response_body = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_body["detail"], "Category name \'Category "
                                                  "1.1.1\' is not unique.")
