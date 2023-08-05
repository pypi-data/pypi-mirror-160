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

class TrackPayload(object):
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
        'token': 'str',
        'customer_properties': 'TrackPayloadCustomerProperties',
        'properties': 'TrackPayloadProperties',
        'time': 'OneOftrackPayloadTime'
    }

    attribute_map = {
        'token': 'token',
        'customer_properties': 'customer_properties',
        'properties': 'properties',
        'time': 'time'
    }

    def __init__(self, token=None, customer_properties=None, properties=None, time=None):  # noqa: E501
        """TrackPayload - a model defined in Swagger"""  # noqa: E501
        self._token = None
        self._customer_properties = None
        self._properties = None
        self._time = None
        self.discriminator = None
        self.token = token
        self.customer_properties = customer_properties
        self.properties = properties
        if time is not None:
            self.time = time

    @property
    def token(self):
        """Gets the token of this TrackPayload.  # noqa: E501


        :return: The token of this TrackPayload.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this TrackPayload.


        :param token: The token of this TrackPayload.  # noqa: E501
        :type: str
        """
        if token is None:
            raise ValueError("Invalid value for `token`, must not be `None`")  # noqa: E501

        self._token = token

    @property
    def customer_properties(self):
        """Gets the customer_properties of this TrackPayload.  # noqa: E501


        :return: The customer_properties of this TrackPayload.  # noqa: E501
        :rtype: TrackPayloadCustomerProperties
        """
        return self._customer_properties

    @customer_properties.setter
    def customer_properties(self, customer_properties):
        """Sets the customer_properties of this TrackPayload.


        :param customer_properties: The customer_properties of this TrackPayload.  # noqa: E501
        :type: TrackPayloadCustomerProperties
        """
        if customer_properties is None:
            raise ValueError("Invalid value for `customer_properties`, must not be `None`")  # noqa: E501

        self._customer_properties = customer_properties

    @property
    def properties(self):
        """Gets the properties of this TrackPayload.  # noqa: E501


        :return: The properties of this TrackPayload.  # noqa: E501
        :rtype: TrackPayloadProperties
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this TrackPayload.


        :param properties: The properties of this TrackPayload.  # noqa: E501
        :type: TrackPayloadProperties
        """
        if properties is None:
            raise ValueError("Invalid value for `properties`, must not be `None`")  # noqa: E501

        self._properties = properties

    @property
    def time(self):
        """Gets the time of this TrackPayload.  # noqa: E501


        :return: The time of this TrackPayload.  # noqa: E501
        :rtype: OneOftrackPayloadTime
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this TrackPayload.


        :param time: The time of this TrackPayload.  # noqa: E501
        :type: OneOftrackPayloadTime
        """

        self._time = time

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
        if issubclass(TrackPayload, dict):
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
        if not isinstance(other, TrackPayload):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
