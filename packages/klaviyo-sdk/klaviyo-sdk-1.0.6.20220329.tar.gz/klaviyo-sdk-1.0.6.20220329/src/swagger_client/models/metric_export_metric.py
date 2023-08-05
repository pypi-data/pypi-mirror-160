# coding: utf-8

"""
    Klaviyo API

    Empowering creators to own their destiny  # noqa: E501

    OpenAPI spec version: 2022.03.29
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MetricExportMetric(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'object': 'str',
        'id': 'str',
        'name': 'str',
        'integration': 'MetricIntegration',
        'created': 'str',
        'updated': 'str'
    }

    attribute_map = {
        'object': 'object',
        'id': 'id',
        'name': 'name',
        'integration': 'integration',
        'created': 'created',
        'updated': 'updated'
    }

    def __init__(self, object=None, id=None, name=None, integration=None, created=None, updated=None):  # noqa: E501
        """MetricExportMetric - a model defined in Swagger"""  # noqa: E501
        self._object = None
        self._id = None
        self._name = None
        self._integration = None
        self._created = None
        self._updated = None
        self.discriminator = None
        if object is not None:
            self.object = object
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if integration is not None:
            self.integration = integration
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated

    @property
    def object(self):
        """Gets the object of this MetricExportMetric.  # noqa: E501


        :return: The object of this MetricExportMetric.  # noqa: E501
        :rtype: str
        """
        return self._object

    @object.setter
    def object(self, object):
        """Sets the object of this MetricExportMetric.


        :param object: The object of this MetricExportMetric.  # noqa: E501
        :type: str
        """

        self._object = object

    @property
    def id(self):
        """Gets the id of this MetricExportMetric.  # noqa: E501


        :return: The id of this MetricExportMetric.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MetricExportMetric.


        :param id: The id of this MetricExportMetric.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this MetricExportMetric.  # noqa: E501


        :return: The name of this MetricExportMetric.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MetricExportMetric.


        :param name: The name of this MetricExportMetric.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def integration(self):
        """Gets the integration of this MetricExportMetric.  # noqa: E501


        :return: The integration of this MetricExportMetric.  # noqa: E501
        :rtype: MetricIntegration
        """
        return self._integration

    @integration.setter
    def integration(self, integration):
        """Sets the integration of this MetricExportMetric.


        :param integration: The integration of this MetricExportMetric.  # noqa: E501
        :type: MetricIntegration
        """

        self._integration = integration

    @property
    def created(self):
        """Gets the created of this MetricExportMetric.  # noqa: E501


        :return: The created of this MetricExportMetric.  # noqa: E501
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this MetricExportMetric.


        :param created: The created of this MetricExportMetric.  # noqa: E501
        :type: str
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this MetricExportMetric.  # noqa: E501


        :return: The updated of this MetricExportMetric.  # noqa: E501
        :rtype: str
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this MetricExportMetric.


        :param updated: The updated of this MetricExportMetric.  # noqa: E501
        :type: str
        """

        self._updated = updated

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if issubclass(MetricExportMetric, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MetricExportMetric):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
