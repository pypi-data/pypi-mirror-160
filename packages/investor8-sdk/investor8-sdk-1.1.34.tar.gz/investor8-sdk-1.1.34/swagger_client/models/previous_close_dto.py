# coding: utf-8

"""
    Investor8.Core

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class PreviousCloseDto(object):
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
        'prev_close_date': 'datetime',
        'prices': 'dict(str, float)'
    }

    attribute_map = {
        'prev_close_date': 'PrevCloseDate',
        'prices': 'Prices'
    }

    def __init__(self, prev_close_date=None, prices=None):  # noqa: E501
        """PreviousCloseDto - a model defined in Swagger"""  # noqa: E501
        self._prev_close_date = None
        self._prices = None
        self.discriminator = None
        if prev_close_date is not None:
            self.prev_close_date = prev_close_date
        if prices is not None:
            self.prices = prices

    @property
    def prev_close_date(self):
        """Gets the prev_close_date of this PreviousCloseDto.  # noqa: E501


        :return: The prev_close_date of this PreviousCloseDto.  # noqa: E501
        :rtype: datetime
        """
        return self._prev_close_date

    @prev_close_date.setter
    def prev_close_date(self, prev_close_date):
        """Sets the prev_close_date of this PreviousCloseDto.


        :param prev_close_date: The prev_close_date of this PreviousCloseDto.  # noqa: E501
        :type: datetime
        """

        self._prev_close_date = prev_close_date

    @property
    def prices(self):
        """Gets the prices of this PreviousCloseDto.  # noqa: E501


        :return: The prices of this PreviousCloseDto.  # noqa: E501
        :rtype: dict(str, float)
        """
        return self._prices

    @prices.setter
    def prices(self, prices):
        """Sets the prices of this PreviousCloseDto.


        :param prices: The prices of this PreviousCloseDto.  # noqa: E501
        :type: dict(str, float)
        """

        self._prices = prices

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
        if issubclass(PreviousCloseDto, dict):
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
        if not isinstance(other, PreviousCloseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
