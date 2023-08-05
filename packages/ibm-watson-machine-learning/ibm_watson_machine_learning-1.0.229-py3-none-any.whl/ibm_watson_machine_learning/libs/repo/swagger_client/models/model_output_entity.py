# coding: utf-8

"""
    IBM Watson Machine Learning REST API

    ## Authorization  ### IBM Watson Machine Learning Credentials (ML Credentials)  The IBM Watson Machine Learning Credentials are available for the Bluemix user for each bound application or requested service key. You will find them in the VCAP information as well you can access them using Cloud Foundry API.  Here is the example of the ML Credentials:  ```json {   \"url\": \"https://ibm-watson-ml.mybluemix.net\",   \"username\": \"c1ef4b80-2ee2-458e-ab92-e9ca97ec657d\",   \"password\": \"edb699da-8595-406e-bae0-74a834fa4d34\",    \"access_key\": \"0uUQPsbQozcci4uwRI7xo0jQnSNOM9YSk....\" } ```  - `url` - the base WML API url - `username` / `password` - the service credentials required to generate the token - `access_key` - the access key used by previous version of the service API (ignored)  The `username` / `password` pair are used to access the Token Endpoint (using HTTP Basic Auth) and obtain the service token (see below). Example:  `curl --basic --user c1ef4b80-2ee2-458e-ab92-e9ca97ec657d:edb699da-8595-406e-bae0-74a834fa4d34 https://ibm-watson-ml.mybluemix.net/v2/identity/token`  ### IBM Watson Machine Learning Token (ML Token)  The IBM Watson Machine Learning REST API is authorized with ML token obtained from the Token Endpoint. The ML token is used as a baerer token send in `authorization` header.  Use WML service credentials (username, password) to gather the token from:   `/v2/identity/token` (see example above).  The token is self-describing JWT (JSON Web Tokens) protected by digital signature for authentication. It holds information required for a service tenant identification. Each ML micro-service is able to verify the token with the public key without request to the token endpoint and firing a database query. The ML service token (ML token) contains the expiration time what simplifies implementation of the access revocation.  ## Spark Instance  The IBM Watson ML co-operates with the Spark as a Service to make calculation and deploy pipeline models. Each API method that requires the Spark service instance accepts a custom header: `X-Spark-Service-Instance` where the Spark instance data like credentials, kernel ID and version can be specified. The header value is a base64 encoded string with the JSON data in the following format:    ```   {     \"credentials\": {       \"tenant_id\": \"sf2c-xxxxx-05b1d10fb12b\",       \"cluster_master_url\": \"https://spark.stage1.bluemix.net\",       \"tenant_id_full\": \"xxxxx-a94d-4f20-bf2c-xxxxxx-xxxx-4c65-a156-05b1d10fb12b\",       \"tenant_secret\": \"xxxx-86fd-40cd-xxx-969aafaeb505\",       \"instance_id\": \"xxx-a94d-xxx-bf2c-xxxx\",       \"plan\": \"ibm.SparkService.PayGoPersonal\"     },     \"version\": \"2.0\",     \"kernelId\": \"xxx-a94d-xxx-bf2c-xxxx\"   }   ```  The fields are: - `credentials` - from the VCAP information of the Spark service instance - `version` - requested Spark version (possible values: 2.0) - `kernelId` (optional) - the Spark kernel ID is only required by actions that operates on running Spark kernel.   This field is redundant when creating any kind of deployment. 

    OpenAPI spec version: 2.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

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

from pprint import pformat
from six import iteritems
import re


class ModelOutputEntity(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, description=None, author=None, type=None, runtime_environment=None, training_data_schema=None, label_col=None, input_data_schema=None, pipeline_version=None, versions_href=None, latest_version=None, output_data_schema=None):
        """
        ModelOutputEntity - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'author': 'ArtifactAuthor',
            'type': 'str',
            'runtime_environment': 'str',
            'training_data_schema': 'object',
            'label_col': 'str',
            'input_data_schema': 'object',
            'pipeline_version': 'ModelOutputEntityPipelineVersion',
            'versions_href': 'str',
            'latest_version': 'ArtifactVersionMetadata',
            'output_data_schema' :'object'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'author': 'author',
            'type': 'type',
            'runtime_environment': 'runtimeEnvironment',
            'training_data_schema': 'trainingDataSchema',
            'label_col': 'labelCol',
            'input_data_schema': 'inputDataSchema',
            'pipeline_version': 'pipelineVersion',
            'versions_href': 'versionsHref',
            'latest_version': 'latestVersion',
            'output_data_schema' : 'outputDataSchema'
        }

        self._name = name
        self._description = description
        self._author = author
        self._type = type
        self._runtime_environment = runtime_environment
        self._training_data_schema = training_data_schema
        self._label_col = label_col
        self._input_data_schema = input_data_schema
        self._pipeline_version = pipeline_version
        self._versions_href = versions_href
        self._latest_version = latest_version
        self._output_data_schema = output_data_schema

    @property
    def name(self):
        """
        Gets the name of this ModelOutputEntity.
        Name of the model

        :return: The name of this ModelOutputEntity.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ModelOutputEntity.
        Name of the model

        :param name: The name of this ModelOutputEntity.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ModelOutputEntity.
        Description of the model

        :return: The description of this ModelOutputEntity.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ModelOutputEntity.
        Description of the model

        :param description: The description of this ModelOutputEntity.
        :type: str
        """

        self._description = description

    @property
    def author(self):
        """
        Gets the author of this ModelOutputEntity.
        Author of the pipeline

        :return: The author of this ModelOutputEntity.
        :rtype: ArtifactAuthor
        """
        return self._author

    @author.setter
    def author(self, author):
        """
        Sets the author of this ModelOutputEntity.
        Author of the pipeline

        :param author: The author of this ModelOutputEntity.
        :type: ArtifactAuthor
        """

        self._author = author

    @property
    def type(self):
        """
        Gets the type of this ModelOutputEntity.
        Type of the ML pipeline model

        :return: The type of this ModelOutputEntity.
        :rtype: ModelType
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ModelOutputEntity.
        Type of the ML pipeline model

        :param type: The type of this ModelOutputEntity.
        :type: ModelType
        """

        self._type = type

    @property
    def runtime_environment(self):
        """
        Gets the runtime_environment of this ModelOutputEntity.
        runtime environment of caller

        :return: The runtime_environment of this ModelOutputEntity.
        :rtype: RuntimeEnvironment
        """
        return self._runtime_environment

    @runtime_environment.setter
    def runtime_environment(self, runtime_environment):
        """
        Sets the runtime_environment of this ModelOutputEntity.
        runtime environment of caller

        :param runtime_environment: The runtime_environment of this ModelOutputEntity.
        :type: RuntimeEnvironment
        """

        self._runtime_environment = runtime_environment

    @property
    def training_data_schema(self):
        """
        Gets the training_data_schema of this ModelOutputEntity.
        JSON schema of the training data

        :return: The training_data_schema of this ModelOutputEntity.
        :rtype: TrainingDataSchema
        """
        return self._training_data_schema

    @training_data_schema.setter
    def training_data_schema(self, training_data_schema):
        """
        Sets the training_data_schema of this ModelOutputEntity.
        JSON schema of the training data

        :param training_data_schema: The training_data_schema of this ModelOutputEntity.
        :type: TrainingDataSchema
        """

        self._training_data_schema = training_data_schema

    @property
    def label_col(self):
        """
        Gets the label_col of this ModelOutputEntity.
        Name of the label column

        :return: The label_col of this ModelOutputEntity.
        :rtype: str
        """
        return self._label_col

    @label_col.setter
    def label_col(self, label_col):
        """
        Sets the label_col of this ModelOutputEntity.
        Name of the label column

        :param label_col: The label_col of this ModelOutputEntity.
        :type: str
        """

        self._label_col = label_col

    @property
    def input_data_schema(self):
        """
        Gets the input_data_schema of this ModelOutputEntity.
        JSON schema of the input data (if not provided the training data schema is used)

        :return: The input_data_schema of this ModelOutputEntity.
        :rtype: InputDataSchema
        """
        return self._input_data_schema

    @input_data_schema.setter
    def input_data_schema(self, input_data_schema):
        """
        Sets the input_data_schema of this ModelOutputEntity.
        JSON schema of the input data (if not provided the training data schema is used)

        :param input_data_schema: The input_data_schema of this ModelOutputEntity.
        :type: InputDataSchema
        """

        self._input_data_schema = input_data_schema

    @property
    def pipeline_version(self):
        """
        Gets the pipeline_version of this ModelOutputEntity.


        :return: The pipeline_version of this ModelOutputEntity.
        :rtype: ModelOutputEntityPipelineVersion
        """
        return self._pipeline_version

    @pipeline_version.setter
    def pipeline_version(self, pipeline_version):
        """
        Sets the pipeline_version of this ModelOutputEntity.


        :param pipeline_version: The pipeline_version of this ModelOutputEntity.
        :type: ModelOutputEntityPipelineVersion
        """

        self._pipeline_version = pipeline_version

    @property
    def versions_href(self):
        """
        Gets the versions_href of this ModelOutputEntity.
        Href to the model versions collection

        :return: The versions_href of this ModelOutputEntity.
        :rtype: str
        """
        return self._versions_href

    @versions_href.setter
    def versions_href(self, versions_href):
        """
        Sets the versions_href of this ModelOutputEntity.
        Href to the model versions collection

        :param versions_href: The versions_href of this ModelOutputEntity.
        :type: str
        """

        self._versions_href = versions_href

    @property
    def latest_version(self):
        """
        Gets the latest_version of this ModelOutputEntity.
        the latest artifact version metadata

        :return: The latest_version of this ModelOutputEntity.
        :rtype: ArtifactVersionMetadata
        """
        return self._latest_version

    @latest_version.setter
    def latest_version(self, latest_version):
        """
        Sets the latest_version of this ModelOutputEntity.
        the latest artifact version metadata

        :param latest_version: The latest_version of this ModelOutputEntity.
        :type: ArtifactVersionMetadata
        """

        self._latest_version = latest_version

    @property
    def output_data_schema(self):
        """
        Gets the output_data_schema of this ModelOutputEntity.
        JSON schema of the output data

        :return: The output_data_schema of this ModelOutputEntity.
        :rtype: OutputDataSchema
        """
        return self._output_data_schema

    @output_data_schema.setter
    def output_data_schema(self, output_data_schema):
        """
        Sets the output_data_schema of this ModelOutputEntity.
        JSON schema of the output data

        :param output_data_schema: The output_data_schema of this ModelOutputEntity.
        :type: OutputDataSchema
        """

        self._output_data_schema = output_data_schema


    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
