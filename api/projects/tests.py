from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from projects.models import Project

class AuthenticatedAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        if cls is not AuthenticatedAPITestCase and cls.setUp is not AuthenticatedAPITestCase.setUp:
            orig_setUp = cls.setUp
            def setUpOverride(self, *args, **kwargs):
                AuthenticatedAPITestCase.setUp(self)
                return orig_setUp(self, *args, **kwargs)
            cls.setUp = setUpOverride

    def setUp(self):
        user = User.objects.create_user('Test', 'test@project.com', 'test')
        token, _ = Token.objects.get_or_create(user=user)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))


class ProjectTest(AuthenticatedAPITestCase):

    def test_create_project(self):
        """
        Creates a project
        """
        # given
        url = '/projects/'

        data = {'name': 'Project 1', 'description': 'This is a description'}

        # when
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, 'Project 1')
        self.assertEqual(Project.objects.get().description, 'This is a description')