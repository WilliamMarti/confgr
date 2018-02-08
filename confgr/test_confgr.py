# project/test_basic.py


import os
import unittest

from confgr import application



class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = False
        application.config['DEBUG'] = False
        self.application = application.test_client()

        self.assertEqual(application.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass

    def login(self, username, password):
        return self.application.post(
            '/login',
            data=dict(username=username, password=password),follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


    ###############
    #### tests ####
    ###############

    def test_main_page(self):
        response = self.application.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_login(self):
        response = self.login('newuser', 'test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'True', response.data)


    def test_invalid_user_login(self):
        response = self.login('baduser', 'test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'False', response.data)


    def test_profile_page(self):

        username = 'newuser'
        response = self.login(username, 'test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'True', response.data)

        response = self.application.get('/profile/' + username, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_page(self):

        username = 'newuser'
        response = self.login(username, 'test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'True', response.data)

        response = self.application.get('/admin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response = self.application.get('/admin/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_create_delete_user(self):

        # Login
        username = 'newuser'
        response = self.login(username, 'test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'True', response.data)

        # Setup user info
        newusername = 'testcaseuser'
        password = 'password'
        first = 'test'
        last = 'case'
        email = 'test@case.com'

        # Create user
        response = self.application.post(
            '/createuser',
            data=dict(username=newusername, password=password, first=first, last=last, email=email),
            follow_redirects=True)

        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Created', response.data)

        # Delete user
        response = self.application.post(
            '/deleteuser',
            data=dict(username=newusername),
            follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Deleted', response.data)


    def test_profile_edit(self):
        pass


    # test 404 page 
    def test_bad_page(self):

        username = 'newuser'
        response = self.login(username, 'test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'True', response.data)

        response = self.application.get('/badpage', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()