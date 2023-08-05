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

class SAAttributesPrices(object):
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
        'identifier': 'str',
        'name': 'str',
        'last': 'float',
        'change': 'float',
        'percent_change': 'float',
        'previous_close': 'float',
        'open': 'float',
        'high': 'float',
        'low': 'float',
        'volume': 'int',
        'date_time': 'str',
        'quote_info': 'str',
        'close': 'float',
        'change_from_previous_close': 'float',
        'percent_change_from_previous_close': 'float',
        'low52_week': 'float',
        'high52_week': 'float',
        'extended_hours_price': 'float',
        'extended_hours_change': 'float',
        'extended_hours_percent_change': 'float',
        'extended_hours_date_time': 'str',
        'extended_hours_type': 'str',
        'source_api': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'name': 'name',
        'last': 'last',
        'change': 'change',
        'percent_change': 'percentChange',
        'previous_close': 'previousClose',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'volume': 'volume',
        'date_time': 'dateTime',
        'quote_info': 'quoteInfo',
        'close': 'close',
        'change_from_previous_close': 'changeFromPreviousClose',
        'percent_change_from_previous_close': 'percentChangeFromPreviousClose',
        'low52_week': 'low52Week',
        'high52_week': 'high52Week',
        'extended_hours_price': 'extendedHoursPrice',
        'extended_hours_change': 'extendedHoursChange',
        'extended_hours_percent_change': 'extendedHoursPercentChange',
        'extended_hours_date_time': 'extendedHoursDateTime',
        'extended_hours_type': 'extendedHoursType',
        'source_api': 'sourceAPI'
    }

    def __init__(self, identifier=None, name=None, last=None, change=None, percent_change=None, previous_close=None, open=None, high=None, low=None, volume=None, date_time=None, quote_info=None, close=None, change_from_previous_close=None, percent_change_from_previous_close=None, low52_week=None, high52_week=None, extended_hours_price=None, extended_hours_change=None, extended_hours_percent_change=None, extended_hours_date_time=None, extended_hours_type=None, source_api=None):  # noqa: E501
        """SAAttributesPrices - a model defined in Swagger"""  # noqa: E501
        self._identifier = None
        self._name = None
        self._last = None
        self._change = None
        self._percent_change = None
        self._previous_close = None
        self._open = None
        self._high = None
        self._low = None
        self._volume = None
        self._date_time = None
        self._quote_info = None
        self._close = None
        self._change_from_previous_close = None
        self._percent_change_from_previous_close = None
        self._low52_week = None
        self._high52_week = None
        self._extended_hours_price = None
        self._extended_hours_change = None
        self._extended_hours_percent_change = None
        self._extended_hours_date_time = None
        self._extended_hours_type = None
        self._source_api = None
        self.discriminator = None
        if identifier is not None:
            self.identifier = identifier
        if name is not None:
            self.name = name
        if last is not None:
            self.last = last
        if change is not None:
            self.change = change
        if percent_change is not None:
            self.percent_change = percent_change
        if previous_close is not None:
            self.previous_close = previous_close
        if open is not None:
            self.open = open
        if high is not None:
            self.high = high
        if low is not None:
            self.low = low
        if volume is not None:
            self.volume = volume
        if date_time is not None:
            self.date_time = date_time
        if quote_info is not None:
            self.quote_info = quote_info
        if close is not None:
            self.close = close
        if change_from_previous_close is not None:
            self.change_from_previous_close = change_from_previous_close
        if percent_change_from_previous_close is not None:
            self.percent_change_from_previous_close = percent_change_from_previous_close
        if low52_week is not None:
            self.low52_week = low52_week
        if high52_week is not None:
            self.high52_week = high52_week
        if extended_hours_price is not None:
            self.extended_hours_price = extended_hours_price
        if extended_hours_change is not None:
            self.extended_hours_change = extended_hours_change
        if extended_hours_percent_change is not None:
            self.extended_hours_percent_change = extended_hours_percent_change
        if extended_hours_date_time is not None:
            self.extended_hours_date_time = extended_hours_date_time
        if extended_hours_type is not None:
            self.extended_hours_type = extended_hours_type
        if source_api is not None:
            self.source_api = source_api

    @property
    def identifier(self):
        """Gets the identifier of this SAAttributesPrices.  # noqa: E501


        :return: The identifier of this SAAttributesPrices.  # noqa: E501
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """Sets the identifier of this SAAttributesPrices.


        :param identifier: The identifier of this SAAttributesPrices.  # noqa: E501
        :type: str
        """

        self._identifier = identifier

    @property
    def name(self):
        """Gets the name of this SAAttributesPrices.  # noqa: E501


        :return: The name of this SAAttributesPrices.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SAAttributesPrices.


        :param name: The name of this SAAttributesPrices.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def last(self):
        """Gets the last of this SAAttributesPrices.  # noqa: E501


        :return: The last of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._last

    @last.setter
    def last(self, last):
        """Sets the last of this SAAttributesPrices.


        :param last: The last of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._last = last

    @property
    def change(self):
        """Gets the change of this SAAttributesPrices.  # noqa: E501


        :return: The change of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._change

    @change.setter
    def change(self, change):
        """Sets the change of this SAAttributesPrices.


        :param change: The change of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._change = change

    @property
    def percent_change(self):
        """Gets the percent_change of this SAAttributesPrices.  # noqa: E501


        :return: The percent_change of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._percent_change

    @percent_change.setter
    def percent_change(self, percent_change):
        """Sets the percent_change of this SAAttributesPrices.


        :param percent_change: The percent_change of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._percent_change = percent_change

    @property
    def previous_close(self):
        """Gets the previous_close of this SAAttributesPrices.  # noqa: E501


        :return: The previous_close of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._previous_close

    @previous_close.setter
    def previous_close(self, previous_close):
        """Sets the previous_close of this SAAttributesPrices.


        :param previous_close: The previous_close of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._previous_close = previous_close

    @property
    def open(self):
        """Gets the open of this SAAttributesPrices.  # noqa: E501


        :return: The open of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._open

    @open.setter
    def open(self, open):
        """Sets the open of this SAAttributesPrices.


        :param open: The open of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._open = open

    @property
    def high(self):
        """Gets the high of this SAAttributesPrices.  # noqa: E501


        :return: The high of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._high

    @high.setter
    def high(self, high):
        """Sets the high of this SAAttributesPrices.


        :param high: The high of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._high = high

    @property
    def low(self):
        """Gets the low of this SAAttributesPrices.  # noqa: E501


        :return: The low of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._low

    @low.setter
    def low(self, low):
        """Sets the low of this SAAttributesPrices.


        :param low: The low of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._low = low

    @property
    def volume(self):
        """Gets the volume of this SAAttributesPrices.  # noqa: E501


        :return: The volume of this SAAttributesPrices.  # noqa: E501
        :rtype: int
        """
        return self._volume

    @volume.setter
    def volume(self, volume):
        """Sets the volume of this SAAttributesPrices.


        :param volume: The volume of this SAAttributesPrices.  # noqa: E501
        :type: int
        """

        self._volume = volume

    @property
    def date_time(self):
        """Gets the date_time of this SAAttributesPrices.  # noqa: E501


        :return: The date_time of this SAAttributesPrices.  # noqa: E501
        :rtype: str
        """
        return self._date_time

    @date_time.setter
    def date_time(self, date_time):
        """Sets the date_time of this SAAttributesPrices.


        :param date_time: The date_time of this SAAttributesPrices.  # noqa: E501
        :type: str
        """

        self._date_time = date_time

    @property
    def quote_info(self):
        """Gets the quote_info of this SAAttributesPrices.  # noqa: E501


        :return: The quote_info of this SAAttributesPrices.  # noqa: E501
        :rtype: str
        """
        return self._quote_info

    @quote_info.setter
    def quote_info(self, quote_info):
        """Sets the quote_info of this SAAttributesPrices.


        :param quote_info: The quote_info of this SAAttributesPrices.  # noqa: E501
        :type: str
        """

        self._quote_info = quote_info

    @property
    def close(self):
        """Gets the close of this SAAttributesPrices.  # noqa: E501


        :return: The close of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._close

    @close.setter
    def close(self, close):
        """Sets the close of this SAAttributesPrices.


        :param close: The close of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._close = close

    @property
    def change_from_previous_close(self):
        """Gets the change_from_previous_close of this SAAttributesPrices.  # noqa: E501


        :return: The change_from_previous_close of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._change_from_previous_close

    @change_from_previous_close.setter
    def change_from_previous_close(self, change_from_previous_close):
        """Sets the change_from_previous_close of this SAAttributesPrices.


        :param change_from_previous_close: The change_from_previous_close of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._change_from_previous_close = change_from_previous_close

    @property
    def percent_change_from_previous_close(self):
        """Gets the percent_change_from_previous_close of this SAAttributesPrices.  # noqa: E501


        :return: The percent_change_from_previous_close of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._percent_change_from_previous_close

    @percent_change_from_previous_close.setter
    def percent_change_from_previous_close(self, percent_change_from_previous_close):
        """Sets the percent_change_from_previous_close of this SAAttributesPrices.


        :param percent_change_from_previous_close: The percent_change_from_previous_close of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._percent_change_from_previous_close = percent_change_from_previous_close

    @property
    def low52_week(self):
        """Gets the low52_week of this SAAttributesPrices.  # noqa: E501


        :return: The low52_week of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._low52_week

    @low52_week.setter
    def low52_week(self, low52_week):
        """Sets the low52_week of this SAAttributesPrices.


        :param low52_week: The low52_week of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._low52_week = low52_week

    @property
    def high52_week(self):
        """Gets the high52_week of this SAAttributesPrices.  # noqa: E501


        :return: The high52_week of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._high52_week

    @high52_week.setter
    def high52_week(self, high52_week):
        """Sets the high52_week of this SAAttributesPrices.


        :param high52_week: The high52_week of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._high52_week = high52_week

    @property
    def extended_hours_price(self):
        """Gets the extended_hours_price of this SAAttributesPrices.  # noqa: E501


        :return: The extended_hours_price of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._extended_hours_price

    @extended_hours_price.setter
    def extended_hours_price(self, extended_hours_price):
        """Sets the extended_hours_price of this SAAttributesPrices.


        :param extended_hours_price: The extended_hours_price of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._extended_hours_price = extended_hours_price

    @property
    def extended_hours_change(self):
        """Gets the extended_hours_change of this SAAttributesPrices.  # noqa: E501


        :return: The extended_hours_change of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._extended_hours_change

    @extended_hours_change.setter
    def extended_hours_change(self, extended_hours_change):
        """Sets the extended_hours_change of this SAAttributesPrices.


        :param extended_hours_change: The extended_hours_change of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._extended_hours_change = extended_hours_change

    @property
    def extended_hours_percent_change(self):
        """Gets the extended_hours_percent_change of this SAAttributesPrices.  # noqa: E501


        :return: The extended_hours_percent_change of this SAAttributesPrices.  # noqa: E501
        :rtype: float
        """
        return self._extended_hours_percent_change

    @extended_hours_percent_change.setter
    def extended_hours_percent_change(self, extended_hours_percent_change):
        """Sets the extended_hours_percent_change of this SAAttributesPrices.


        :param extended_hours_percent_change: The extended_hours_percent_change of this SAAttributesPrices.  # noqa: E501
        :type: float
        """

        self._extended_hours_percent_change = extended_hours_percent_change

    @property
    def extended_hours_date_time(self):
        """Gets the extended_hours_date_time of this SAAttributesPrices.  # noqa: E501


        :return: The extended_hours_date_time of this SAAttributesPrices.  # noqa: E501
        :rtype: str
        """
        return self._extended_hours_date_time

    @extended_hours_date_time.setter
    def extended_hours_date_time(self, extended_hours_date_time):
        """Sets the extended_hours_date_time of this SAAttributesPrices.


        :param extended_hours_date_time: The extended_hours_date_time of this SAAttributesPrices.  # noqa: E501
        :type: str
        """

        self._extended_hours_date_time = extended_hours_date_time

    @property
    def extended_hours_type(self):
        """Gets the extended_hours_type of this SAAttributesPrices.  # noqa: E501


        :return: The extended_hours_type of this SAAttributesPrices.  # noqa: E501
        :rtype: str
        """
        return self._extended_hours_type

    @extended_hours_type.setter
    def extended_hours_type(self, extended_hours_type):
        """Sets the extended_hours_type of this SAAttributesPrices.


        :param extended_hours_type: The extended_hours_type of this SAAttributesPrices.  # noqa: E501
        :type: str
        """

        self._extended_hours_type = extended_hours_type

    @property
    def source_api(self):
        """Gets the source_api of this SAAttributesPrices.  # noqa: E501


        :return: The source_api of this SAAttributesPrices.  # noqa: E501
        :rtype: str
        """
        return self._source_api

    @source_api.setter
    def source_api(self, source_api):
        """Sets the source_api of this SAAttributesPrices.


        :param source_api: The source_api of this SAAttributesPrices.  # noqa: E501
        :type: str
        """

        self._source_api = source_api

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
        if issubclass(SAAttributesPrices, dict):
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
        if not isinstance(other, SAAttributesPrices):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
