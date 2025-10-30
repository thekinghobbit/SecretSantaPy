import unittest

import email
import logging
from unittest.mock import patch
from Secret_Santa import *
RECIPIENTS = ['a@gmail.com', 'b@gmail.com', 'c@gmail.com', 'd@gmail.com']
def repeat(times):
    def repeatHelper(f):
        def callHelper(*args, **kwargs):
            for _ in range(times):
                f(*args, **kwargs)
        return callHelper
    return repeatHelper

class TestSecretSanta(unittest.TestCase):
    @repeat(100)
    def test_no_self_assignment(self):
        messages = create_assignment_list(RECIPIENTS.copy())
        for msg in messages:
            self.assertNotEqual(msg.get_content().split()[4], msg['To'])

    @repeat(100)
    def test_all_assignment(self):
        messages = create_assignment_list(RECIPIENTS.copy())        
        for msg in messages:
            self.assertIn(msg.get_content().split()[4], RECIPIENTS)

if __name__ == '__main__':
    unittest.main()