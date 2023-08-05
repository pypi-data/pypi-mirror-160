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

class MetricsMetadataResponseDto(object):
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
        'metric_name': 'str',
        'display_name': 'str',
        'data_format': 'str',
        'display_format': 'str',
        'default_period_type': 'str'
    }

    attribute_map = {
        'metric_name': 'MetricName',
        'display_name': 'DisplayName',
        'data_format': 'DataFormat',
        'display_format': 'DisplayFormat',
        'default_period_type': 'DefaultPeriodType'
    }

    def __init__(self, metric_name=None, display_name=None, data_format=None, display_format=None, default_period_type=None):  # noqa: E501
        """MetricsMetadataResponseDto - a model defined in Swagger"""  # noqa: E501
        self._metric_name = None
        self._display_name = None
        self._data_format = None
        self._display_format = None
        self._default_period_type = None
        self.discriminator = None
        if metric_name is not None:
            self.metric_name = metric_name
        if display_name is not None:
            self.display_name = display_name
        if data_format is not None:
            self.data_format = data_format
        if display_format is not None:
            self.display_format = display_format
        if default_period_type is not None:
            self.default_period_type = default_period_type

    @property
    def metric_name(self):
        """Gets the metric_name of this MetricsMetadataResponseDto.  # noqa: E501


        :return: The metric_name of this MetricsMetadataResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._metric_name

    @metric_name.setter
    def metric_name(self, metric_name):
        """Sets the metric_name of this MetricsMetadataResponseDto.


        :param metric_name: The metric_name of this MetricsMetadataResponseDto.  # noqa: E501
        :type: str
        """

        self._metric_name = metric_name

    @property
    def display_name(self):
        """Gets the display_name of this MetricsMetadataResponseDto.  # noqa: E501


        :return: The display_name of this MetricsMetadataResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """Sets the display_name of this MetricsMetadataResponseDto.


        :param display_name: The display_name of this MetricsMetadataResponseDto.  # noqa: E501
        :type: str
        """

        self._display_name = display_name

    @property
    def data_format(self):
        """Gets the data_format of this MetricsMetadataResponseDto.  # noqa: E501


        :return: The data_format of this MetricsMetadataResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._data_format

    @data_format.setter
    def data_format(self, data_format):
        """Sets the data_format of this MetricsMetadataResponseDto.


        :param data_format: The data_format of this MetricsMetadataResponseDto.  # noqa: E501
        :type: str
        """

        self._data_format = data_format

    @property
    def display_format(self):
        """Gets the display_format of this MetricsMetadataResponseDto.  # noqa: E501


        :return: The display_format of this MetricsMetadataResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._display_format

    @display_format.setter
    def display_format(self, display_format):
        """Sets the display_format of this MetricsMetadataResponseDto.


        :param display_format: The display_format of this MetricsMetadataResponseDto.  # noqa: E501
        :type: str
        """

        self._display_format = display_format

    @property
    def default_period_type(self):
        """Gets the default_period_type of this MetricsMetadataResponseDto.  # noqa: E501


        :return: The default_period_type of this MetricsMetadataResponseDto.  # noqa: E501
        :rtype: str
        """
        return self._default_period_type

    @default_period_type.setter
    def default_period_type(self, default_period_type):
        """Sets the default_period_type of this MetricsMetadataResponseDto.


        :param default_period_type: The default_period_type of this MetricsMetadataResponseDto.  # noqa: E501
        :type: str
        """

        self._default_period_type = default_period_type

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
        if issubclass(MetricsMetadataResponseDto, dict):
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
        if not isinstance(other, MetricsMetadataResponseDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
