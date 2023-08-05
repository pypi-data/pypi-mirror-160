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

class ListIdMembersBody1(object):
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
        'emails': 'list[str]',
        'phone_numbers': 'list[str]',
        'push_tokens': 'list[str]'
    }

    attribute_map = {
        'emails': 'emails',
        'phone_numbers': 'phone_numbers',
        'push_tokens': 'push_tokens'
    }

    def __init__(self, emails=None, phone_numbers=None, push_tokens=None):  # noqa: E501
        """ListIdMembersBody1 - a model defined in Swagger"""  # noqa: E501
        self._emails = None
        self._phone_numbers = None
        self._push_tokens = None
        self.discriminator = None
        if emails is not None:
            self.emails = emails
        if phone_numbers is not None:
            self.phone_numbers = phone_numbers
        if push_tokens is not None:
            self.push_tokens = push_tokens

    @property
    def emails(self):
        """Gets the emails of this ListIdMembersBody1.  # noqa: E501


        :return: The emails of this ListIdMembersBody1.  # noqa: E501
        :rtype: list[str]
        """
        return self._emails

    @emails.setter
    def emails(self, emails):
        """Sets the emails of this ListIdMembersBody1.


        :param emails: The emails of this ListIdMembersBody1.  # noqa: E501
        :type: list[str]
        """

        self._emails = emails

    @property
    def phone_numbers(self):
        """Gets the phone_numbers of this ListIdMembersBody1.  # noqa: E501


        :return: The phone_numbers of this ListIdMembersBody1.  # noqa: E501
        :rtype: list[str]
        """
        return self._phone_numbers

    @phone_numbers.setter
    def phone_numbers(self, phone_numbers):
        """Sets the phone_numbers of this ListIdMembersBody1.


        :param phone_numbers: The phone_numbers of this ListIdMembersBody1.  # noqa: E501
        :type: list[str]
        """

        self._phone_numbers = phone_numbers

    @property
    def push_tokens(self):
        """Gets the push_tokens of this ListIdMembersBody1.  # noqa: E501


        :return: The push_tokens of this ListIdMembersBody1.  # noqa: E501
        :rtype: list[str]
        """
        return self._push_tokens

    @push_tokens.setter
    def push_tokens(self, push_tokens):
        """Sets the push_tokens of this ListIdMembersBody1.


        :param push_tokens: The push_tokens of this ListIdMembersBody1.  # noqa: E501
        :type: list[str]
        """

        self._push_tokens = push_tokens

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
        if issubclass(ListIdMembersBody1, dict):
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
        if not isinstance(other, ListIdMembersBody1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
