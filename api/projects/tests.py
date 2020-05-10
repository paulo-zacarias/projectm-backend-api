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

        user_2 = User.objects.create_user('Test2', 'test2@project.com', 'test2')
        user_2.save()

        project = Project(name='Project', description='Project description', admin=user)
        project.save()


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
        self.assertEqual(Project.objects.count(), 2)
        project = Project.objects.get(id=2)
        self.assertEqual(project.name, 'Project 1')
        self.assertEqual(project.description, 'This is a description')
        self.assertEqual(project.admin.username, 'Test')
        self.assertEqual(project.participants.all().count(), 0)

    def test_create_un_authenticated(self):
        """
        Creates a project
        """
        # given
        url = '/projects/'

        data = {'name': 'Project 1', 'description': 'This is a description'}

        self.client.force_authenticate(user=None)

        # when
        response = self.client.post(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_by_project_admin(self):
        """
        Creates a project
        """
        # given
        url = '/projects/1/'

        data = {'name': 'Project', 'description': 'Updated project description'}
        self.client.post(url, data, format='json')

        # when
        response = self.client.put(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.get().description, 'Updated project description')

    def test_update_by_non_project_admin(self):
        """
        Creates a project
        """
        # given
        url = '/projects/1/'

        data = {'name': 'Project 1', 'description': 'Unauthorized description'}

        token, _ = Token.objects.get_or_create(user=User.objects.get(id=2))

        self.client.credentials(HTTP_AUTHORIZATION='Token {}'.format(token))

        # when
        response_get = self.client.get(url)
        response_put = self.client.put(url, data, format='json')

        # assert
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_put.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_project_list(self):
        """
        Creates a project
        """
        # given
        url = '/projects/'

        # when
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_project_list_un_authenticated(self):
        """
        Creates a project
        """
        # given
        url = '/projects/'

        self.client.force_authenticate(user=None)

        # when
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_project(self):
        """
        Creates a project
        """
        # given
        url = '/projects/1/'

        # when
        response = self.client.get(url)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Project')
        self.assertEqual(response.data['description'], 'Project description')

    def test_add_participants(self):
        """
        Creates a project
        """
        # given
        url = '/projects/1/'

        data = {'name': 'Project', 'description': 'Project description', 'participants': [1, 2]}

        # when
        response = self.client.put(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = Project.objects.get(id=1)
        self.assertEqual(project.participants.all().count(), 2)

    def test_add_participants_non_existent_user(self):
        """
        Creates a project
        """
        # given
        url = '/projects/1/'

        data = {'name': 'Project', 'description': 'Project description', 'participants': [1, 2, 3]}

        # when
        response = self.client.put(url, data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
