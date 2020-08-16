import unittest
import requests
import random
import string
import json


class ApiUnit(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.url = 'http://localhost:8080/unit'
        self.headers = {'Accept': 'application/json',
                        'Authorization': 'QWRtaW4=:IXBhc3N3b3JkMQ==',
                        'Content-Type': 'application/x-www-form-urlencoded'}
        letters = string.ascii_lowercase
        self.unitrandomadditionals = "Unit" + ''.join(random.choice(letters) for i in range(4))

    def test_1POST_UNIT(self):
        data = {'name': self.unitrandomadditionals
                }
        post = requests.post(self.url, headers=self.headers, data=data)
        json_data = json.loads(post.text)
        self.assertEqual(post.status_code, 200)
        self.assertEqual(json_data['Success'], True)
        if post.status_code == 200 and json_data['Success']:
            getids = requests.get(self.url, headers=self.headers)
            json_data = json.loads(getids.text)
            id = json_data['Data'][len(json_data['Data'])-1]['Id']
            resp = requests.get(self.url+"/"+str(id), headers=self.headers)
            json_data = json.loads(resp.text)
            self.assertEqual((json_data['Data']['Name']), self.unitrandomadditionals)


    def test_2GET_UNIT(self):
        resp = requests.get(self.url, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        json_data = json.loads(resp.text)
        self.assertEqual((json_data['Data'][len(json_data['Data'])-1]['Name']), self.unitrandomadditionals)

    def test_3GET_ID_UNIT(self):
        resp = requests.get(self.url, headers=self.headers)
        json_data = json.loads(resp.text)
        for x in range(1, len(json_data['Data']) + 1):
            if x == len(json_data['Data']) + 1:
                id = json_data['Data'][x - 1]['Id']
                resp1 = requests.get(self.url + "/" + str(id + 1), headers=self.headers)
                self.assertEqual(resp1.status_code, 404)
                break
            else:
                id = json_data['Data'][x - 1]['Id']
                resp1 = requests.get(self.url + "/" + str(id), headers=self.headers)
                json_dataID = json.loads(resp1.text)
                self.assertEqual(resp1.status_code, 200)
                self.assertEqual((json_dataID['Data']['Id']), id)


    def test_4PUT_UNIT(self):
        data = {'name': "PutUnit"
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
            self.assertEqual((json_data['Data']['Name']), "PutUnit")

    def test_5DELETE_UNIT(self):
        data = {'name': 'deletetest'
                }
        post = requests.post(self.url, headers=self.headers, data=data)
        resp = requests.get(self.url, headers=self.headers)
        json_data = json.loads(resp.text)
        id = json_data['Data'][len(json_data['Data'])-1]['Id']
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