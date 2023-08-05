#  (C) Copyright IBM Corp. 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest

from ibm_watson_machine_learning.workspace import WorkSpace
from ibm_watson_machine_learning import APIClient
from ibm_watson_machine_learning.tests.utils import get_wml_credentials


class TestWorkSpace(unittest.TestCase):
    workspace: 'WorkSpace' = None

    wml_credentials = None
    project_id = None
    space_id = None

    @classmethod
    def setUp(cls) -> None:
        cls.wml_credentials = get_wml_credentials()
        cls.project_id = None
        cls.space_id = None

    def test__01__initialize_WorkSpace_object__all_properties_set(self):
        TestWorkSpace.workspace = WorkSpace(wml_credentials=self.wml_credentials,
                                            project_id=self.project_id,
                                            space_id=self.space_id)

        self.assertEqual(self.workspace.space_id, self.space_id, msg="Space_id set incorrectly.")
        self.assertEqual(self.workspace.project_id, self.project_id, msg="Project_id set incorrectly.")
        self.assertEqual(self.workspace.wml_credentials, self.wml_credentials, msg="WML credentials set incorrectly.")
        self.assertIsInstance(self.workspace.wml_client, APIClient,
                              msg="WML client is not initialized.")


if __name__ == '__main__':
    unittest.main()
