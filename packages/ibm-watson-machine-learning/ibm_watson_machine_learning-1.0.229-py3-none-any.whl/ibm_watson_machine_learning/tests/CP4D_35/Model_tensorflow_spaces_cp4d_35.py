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
import logging
from ibm_watson_machine_learning.wml_client_error import ApiRequestFailure
from ibm_watson_machine_learning.tests.CP4D_35.preparation_and_cleaning import *


class TestWMLClientWithTF(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    scoring_url = None
    scoring_uid = None
    logger = logging.getLogger(__name__)

    @classmethod
    def setUpClass(self):
        TestWMLClientWithTF.logger.info("Service Instance: setting up credentials")

        self.wml_credentials = get_wml_credentials()
        self.client = get_client()





        self.space_name = str(uuid.uuid4())

        metadata = {
            self.client.spaces.ConfigurationMetaNames.NAME: 'client_space_' + self.space_name,
            self.client.spaces.ConfigurationMetaNames.DESCRIPTION: self.space_name + ' description'
        }

        self.space = self.client.spaces.store(meta_props=metadata)

        TestWMLClientWithTF.space_id = self.client.spaces.get_id(self.space)
        print("space_id: ", TestWMLClientWithTF.space_id)
        self.client.set.default_space(TestWMLClientWithTF.space_id)

    def test_01_publish_local_model_in_repository(self):

        self.client.repository.ModelMetaNames.show()

        model_content_path = 'artifacts/tf_model_fvt_test.tar.gz'
        sw_spec_id = self.client.software_specifications.get_uid_by_name('default_py3.7')

        model_details = self.client.repository.store_model(model=model_content_path,
                                                           meta_props={self.client.repository.ModelMetaNames.NAME: "test_tf",
                                                                  self.client.repository.ModelMetaNames.SOFTWARE_SPEC_UID: sw_spec_id,
                                                                  self.client.repository.ModelMetaNames.TYPE: 'tensorflow_2.1'})
        TestWMLClientWithTF.model_id = self.client.repository.get_model_uid(model_details)

        print(TestWMLClientWithTF.model_id)

        self.assertIsNotNone(TestWMLClientWithTF.model_id)

    def test_02_get_details(self):
        TestWMLClientWithTF.logger.info("Get details")
        self.assertIsNotNone(self.client.repository.get_details(TestWMLClientWithTF.model_id))

    def test_03_create_deployment(self):
        TestWMLClientWithTF.logger.info("Create deployment")
        deployment_details = self.client.deployments.create(TestWMLClientWithTF.model_id,
                                                            meta_props={self.client.deployments.ConfigurationMetaNames.NAME: "Test TF deployment",
                                                                        self.client.deployments.ConfigurationMetaNames.ONLINE:{}})

        TestWMLClientWithTF.logger.debug("Deployment details: {}".format(deployment_details))

        TestWMLClientWithTF.deployment_id = self.client.deployments.get_id(deployment_details)

        TestWMLClientWithTF.scoring_url = self.client.deployments.get_scoring_href(deployment_details)
        TestWMLClientWithTF.logger.debug("Scoring url: {}".format(TestWMLClientWithTF.scoring_url))

        self.assertTrue('online' in str(deployment_details))

    def test_04_get_deployment_details(self):
        TestWMLClientWithTF.logger.info("Get deployment details")
        deployment_details = self.client.deployments.get_details(deployment_uid=TestWMLClientWithTF.deployment_id)
        self.assertIsNotNone(deployment_details)

    def test_05_delete_model(self):
        TestWMLClientWithTF.logger.info("Delete model")
        self.client.repository.delete(TestWMLClientWithTF.model_id)

    def test_06_delete_space(self):
        TestWMLClientWithTF.logger.info("Delete space")
        self.client.spaces.delete(TestWMLClientWithTF.space_id)

if __name__ == '__main__':
    unittest.main()
