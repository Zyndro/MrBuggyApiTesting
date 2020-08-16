import unittest
import requests
import random
import string
import json

class ApiUser(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.url = 'http://localhost:8080/user'
        self.headers = {'Accept': 'application/json',
                        'Authorization': 'QWRtaW4=:IXBhc3N3b3JkMQ==',
                        'Content-Type': 'application/x-www-form-urlencoded'}
        letters = string.ascii_lowercase
        self.adminrandomadditionals = "Admin"+''.join(random.choice(letters) for i in range(4))
        self.employeerandomadditionals = "Employeer" + ''.join(random.choice(letters) for i in range(4))
        self.providerrandomadditionals = "Provider" + ''.join(random.choice(letters) for i in range(4))



    def test_1GET_USER(self):
        resp = requests.get(self.url, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        json_data = json.loads(resp.text)
        self.assertEqual((json_data['Data'][len(json_data['Data'])-1]['Username']), "Admin")

    def test_2GET_ID_USER(self):
        resp = requests.get(self.url, headers=self.headers)
        json_data = json.loads(resp.text)
        for x in range(1,len(json_data['Data'])+1):
                if x == len(json_data['Data'])+1:
                    id = json_data['Data'][x - 1]['Id']
                    resp1 = requests.get(self.url + "/" + str(id+1), headers=self.headers)
                    self.assertEqual(resp1.status_code, 404)
                    break
                else:
                    id = json_data['Data'][x-1]['Id']
                    resp1 = requests.get(self.url+"/"+str(id), headers=self.headers)
                    json_dataID = json.loads(resp1.text)
                    self.assertEqual(resp1.status_code, 200)
                    self.assertEqual((json_dataID['Data']['Id']), id)


    def test_3GET_PROFILE_USER(self):
        resp = requests.get(self.url+"/profile", headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        json_data = json.loads(resp.text)
        self.assertEqual((json_data['Data']['Id']), 1)
        self.assertEqual((json_data['Data']['Role']), "Admin")
        self.assertEqual((json_data['Data']['Status']), "Active")
        self.assertEqual((json_data['Data']['Username']), "Admin")
        self.assertEqual((json_data['Data']['FirstName']), "First")
        self.assertEqual((json_data['Data']['LastName']), "Admin")


    def test_4POST_Admin_USER(self):
        data = {'first_name': self.adminrandomadditionals,
                'username': self.adminrandomadditionals,
                'last_name': self.adminrandomadditionals,
                'email': 'python@com.com',
                'phone_number': '12345678123',
                'password': '!password1'
                }

        post = requests.post(self.url + "/admin", headers=self.headers, data=data)
        json_data = json.loads(post.text)
        self.assertEqual(post.status_code, 200)
        self.assertEqual(json_data['Success'], True)
        if post.status_code == 200 and json_data['Success']:
            getids = requests.get(self.url, headers=self.headers)
            json_data = json.loads(getids.text)
            id = json_data['Data'][0]['Id']
            resp = requests.get(self.url+"/"+str(id), headers=self.headers)
            json_data = json.loads(resp.text)
            self.assertEqual((json_data['Data']['Role']), "Admin")
            self.assertEqual((json_data['Data']['Status']), "Active")
            self.assertEqual((json_data['Data']['Username']), self.adminrandomadditionals)
            self.assertEqual((json_data['Data']['FirstName']), self.adminrandomadditionals)
            self.assertEqual((json_data['Data']['LastName']), self.adminrandomadditionals)
            self.assertEqual((json_data['Data']['PhoneNumber']), "12345678123")
            self.assertEqual((json_data['Data']['Email']), "python@com.com")

    def test_5POST__Employee_USER(self):
        data = {'first_name': self.employeerandomadditionals,
                'username': self.employeerandomadditionals,
                'last_name': self.employeerandomadditionals,
                'email': 'python@com.com',
                'phone_number': '12345678123',
                'password': '!password2',
                'unit_id': '1'
                }

        post = requests.post(self.url + "/employee", headers=self.headers, data=data)
        json_data = json.loads(post.text)
        self.assertEqual(post.status_code, 200)
        self.assertEqual(json_data['Success'], True)
        if post.status_code == 200 and json_data['Success']:
            resp = requests.get(self.url, headers=self.headers)
            json_data = json.loads(resp.text)
            id = json_data['Data'][0]['Id']
            resp = requests.get(self.url+"/"+str(id), headers=self.headers)
            json_data = json.loads(resp.text)
            self.assertEqual((json_data['Data']['Role']), "Employee")
            self.assertEqual((json_data['Data']['Status']), "Active")
            self.assertEqual((json_data['Data']['Username']),self.employeerandomadditionals)
            self.assertEqual((json_data['Data']['FirstName']), self.employeerandomadditionals)
            self.assertEqual((json_data['Data']['LastName']), self.employeerandomadditionals)
            self.assertEqual((json_data['Data']['PhoneNumber']), "12345678123")
            self.assertEqual((json_data['Data']['Email']), "python@com.com")



    def test_6POST__Provider_USER(self):
        data = {'first_name': self.providerrandomadditionals,
                'username': self.providerrandomadditionals,
                'last_name': self.providerrandomadditionals,
                'email': 'python@com.com',
                'phone_number': '12345678123',
                'password': '!password2',
                'provider_id': '1'
                }

        post = requests.post(self.url + "/provider", headers=self.headers, data=data)
        json_data = json.loads(post.text)
        self.assertEqual(post.status_code, 200)
        self.assertEqual(json_data['Success'], True)
        if post.status_code == 200 and json_data['Success']:
            resp = requests.get(self.url, headers=self.headers)
            json_data = json.loads(resp.text)
            id = json_data['Data'][0]['Id']
            resp = requests.get(self.url + "/" + str(id), headers=self.headers)
            json_data = json.loads(resp.text)
            self.assertEqual((json_data['Data']['Role']), "Provider")
            self.assertEqual((json_data['Data']['Status']), "Active")
            self.assertEqual((json_data['Data']['Username']), self.providerrandomadditionals)
            self.assertEqual((json_data['Data']['FirstName']), self.providerrandomadditionals)
            self.assertEqual((json_data['Data']['LastName']), self.providerrandomadditionals)
            self.assertEqual((json_data['Data']['PhoneNumber']), "12345678123")
            self.assertEqual((json_data['Data']['Email']), "python@com.com")

    def test_7PUT_USER(self):
        data = {'first_name': "PutNewUser",
                'last_name': 'PutNewUserLast',
                'email': 'Putpython@com.co',
                'phone_number': '02345678123'
                }
        resp = requests.get(self.url, headers=self.headers)
        json_data = json.loads(resp.text)
        id = json_data['Data'][0]['Id']
        put = requests.get(self.url + "/" + str(id), headers=self.headers, data=data)
        json_data = json.loads(put.text)
        self.assertEqual(put.status_code, 200)
        self.assertEqual(json_data['Success'], True)
        if put.status_code == 200 and json_data['Success']:
            getids = requests.get(self.url, headers=self.headers)
            json_data = json.loads(getids.text)
            id = json_data['Data'][0]['Id']
            resp = requests.get(self.url + "/" + str(id), headers=self.headers)
            json_data = json.loads(resp.text)
            self.assertEqual((json_data['Data']['FirstName']), "PutNewUser")
            self.assertEqual((json_data['Data']['LastName']), "PutNewUserLast")
            self.assertEqual((json_data['Data']['PhoneNumber']), "02345678123")
            self.assertEqual((json_data['Data']['Email']), "Putpython@com.com")

    def test_8PUT_USER_USER(self):
        data = {'first_name': "PutNewAdmin",
                'last_name': 'PutNewAdminLast'
                }
        put = requests.get(self.url + "/profile", headers=self.headers, data=data)
        json_data = json.loads(put.text)
        self.assertEqual(put.status_code, 200)
        self.assertEqual(json_data['Success'], True)
        if put.status_code == 200 and json_data['Success']:
            resp = requests.get(self.url + "/profile", headers=self.headers)
            json_data = json.loads(resp.text)
            self.assertEqual((json_data['Data']['FirstName']), "PutNewAdmin")
            self.assertEqual((json_data['Data']['LastName']), "PutNewAdminLast")
    
    def test_9DELETE_USER(self):
        resp = requests.get(self.url, headers=self.headers)
        json_data = json.loads(resp.text)
        id = json_data['Data'][1]['Id']
        delete = requests.delete(self.url + "/" + str(id), headers=self.headers)
        json_data = json.loads(delete.text)
        self.assertEqual(delete.status_code, 200)
        self.assertEqual(json_data['Success'], True)
        if delete.status_code == 200 and json_data['Success']:
            get = requests.get(self.url + "/" + str(id), headers=self.headers)
            self.assertEqual(get.status_code, 404)


    @classmethod
    def tearDownClass(self):
        pass


if __name__ == '__main__':
    unittest.main()