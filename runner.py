import unittest
from datetime import datetime
from tests.TestApiUsers import ApiUser
from tests.TestApiUnit import ApiUnit
from tests.TestApiProvider import ApiProvider

ApiUser = unittest.TestLoader().loadTestsFromTestCase(ApiUser)
ApiUnit = unittest.TestLoader().loadTestsFromTestCase(ApiUnit)
ApiProvider = unittest.TestLoader().loadTestsFromTestCase(ApiProvider)

suite = unittest.TestSuite([
    ApiUnit,
    ApiProvider,
    ApiUser
])


if __name__ == '__main__':
   now = datetime.now()
   datetime = now.strftime("%d.%m.%Y_%H-%M-%S")
   log_file = 'API_TESTREPORT_'+datetime+'.txt'
   with open(log_file, "w") as f:
       runner = unittest.TextTestRunner(f, verbosity=2)
       result = runner.run(suite)


