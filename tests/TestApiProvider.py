import unittest
import requests
import random
import string
import json


class ApiProvider(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.url = 'http://localhost:8080/provider'
        self.headers = {'Accept': 'application/json',
                        'Authorization': 'QWRtaW4=:IXBhc3N3b3JkMQ==',
                        'Content-Type': 'application/x-www-form-urlencoded'}
        letters = string.ascii_lowercase
        self.providerrandomadditionals = "Provider" + ''.join(random.choice(letters) for i in range(4))

    def test_1POST_PROVIDER(self):
        data = {'name': self.providerrandomadditionals,
                'price': '100'
                }
        post = requests.post(self.url, headers=self.headers, data=data)
        json_data = json.loads(post.text)
        self.assertEqual(post.status_code, 200)
        self.assertEqual(json_data['Success'], True)
        if post.status_code == 200 and json_data['Success']:
            getids = requests.get(self.url, headers=self.headers)
            json_data = json.loads(getids.text)
            results = [x for x in json_data['Data'] if 'Id' in x]
            sort = sorted(results, key=lambda x: x['Id'])
            id = sort[len(sort)-1]['Id']
            resp = requests.get(self.url+"/"+str(id), headers=self.headers)
            json_data = json.loads(resp.text)
            self.assertEqual((json_data['Data']['Name']), self.providerrandomadditionals)
            self.assertEqual((json_data['Data']['Price']), 100)

    def test_2GET_PROVIDER(self):
        resp = requests.get(self.url, headers=self.headers)
        self.assertEqual(resp.status_code, 200)
        json_data = json.loads(resp.text)
        results = [x for x in json_data['Data'] if 'Id' in x]
        sort = sorted(results, key=lambda x: x['Id'])
        getname = sort[len(sort) - 1]['Name']
        self.assertEqual(getname, self.providerrandomadditionals)

    def test_3GET_ID_PROVIDER(self):
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


    def test_4PUT_PROVIDER(self):
        data = {'name': "PutProvider",
                'price': 120
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
            self.assertEqual((json_data['Data']['Price']), 120)

    def test_5DELETE_PROVIDER(self):
        data = {'name': 'deletetest',
                'price': 150
                }
        post = requests.post(self.url, headers=self.headers, data=data)
        resp = requests.get(self.url, headers=self.headers)
        json_data = json.loads(resp.text)
        results = [x for x in json_data['Data'] if 'Id' in x]
        sort = sorted(results, key=lambda x: x['Id'])
        id = sort[len(sort) - 1]['Id']
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