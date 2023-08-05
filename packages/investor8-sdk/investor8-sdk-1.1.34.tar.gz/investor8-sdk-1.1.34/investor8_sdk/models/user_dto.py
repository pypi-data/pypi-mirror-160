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

class UserDto(object):
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
        'user_id': 'str',
        'first_name': 'str',
        'last_name': 'str',
        'email': 'str',
        'roles': 'list[str]',
        'opt_for_newsletter': 'bool',
        'country': 'str',
        'email_confirmed': 'bool',
        'created_time': 'int',
        'last_modified': 'int',
        'profile_name': 'ProfileName',
        'api_key': 'str',
        'token': 'str',
        'premium_start_date': 'datetime',
        'charging_start_date': 'datetime',
        'charging_next_date': 'datetime',
        'cancel_date': 'datetime',
        'auth_source': 'AuthenticationSource',
        'subscription_id': 'str',
        'referer': 'str',
        'allow_terminal_logging': 'bool',
        'stripe_customer_id': 'str'
    }

    attribute_map = {
        'user_id': 'UserId',
        'first_name': 'FirstName',
        'last_name': 'LastName',
        'email': 'Email',
        'roles': 'Roles',
        'opt_for_newsletter': 'OptForNewsletter',
        'country': 'Country',
        'email_confirmed': 'EmailConfirmed',
        'created_time': 'CreatedTime',
        'last_modified': 'LastModified',
        'profile_name': 'ProfileName',
        'api_key': 'ApiKey',
        'token': 'Token',
        'premium_start_date': 'PremiumStartDate',
        'charging_start_date': 'ChargingStartDate',
        'charging_next_date': 'ChargingNextDate',
        'cancel_date': 'CancelDate',
        'auth_source': 'AuthSource',
        'subscription_id': 'SubscriptionId',
        'referer': 'Referer',
        'allow_terminal_logging': 'AllowTerminalLogging',
        'stripe_customer_id': 'StripeCustomerId'
    }

    def __init__(self, user_id=None, first_name=None, last_name=None, email=None, roles=None, opt_for_newsletter=None, country=None, email_confirmed=None, created_time=None, last_modified=None, profile_name=None, api_key=None, token=None, premium_start_date=None, charging_start_date=None, charging_next_date=None, cancel_date=None, auth_source=None, subscription_id=None, referer=None, allow_terminal_logging=None, stripe_customer_id=None):  # noqa: E501
        """UserDto - a model defined in Swagger"""  # noqa: E501
        self._user_id = None
        self._first_name = None
        self._last_name = None
        self._email = None
        self._roles = None
        self._opt_for_newsletter = None
        self._country = None
        self._email_confirmed = None
        self._created_time = None
        self._last_modified = None
        self._profile_name = None
        self._api_key = None
        self._token = None
        self._premium_start_date = None
        self._charging_start_date = None
        self._charging_next_date = None
        self._cancel_date = None
        self._auth_source = None
        self._subscription_id = None
        self._referer = None
        self._allow_terminal_logging = None
        self._stripe_customer_id = None
        self.discriminator = None
        self.user_id = user_id
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email
        if roles is not None:
            self.roles = roles
        if opt_for_newsletter is not None:
            self.opt_for_newsletter = opt_for_newsletter
        if country is not None:
            self.country = country
        if email_confirmed is not None:
            self.email_confirmed = email_confirmed
        if created_time is not None:
            self.created_time = created_time
        if last_modified is not None:
            self.last_modified = last_modified
        if profile_name is not None:
            self.profile_name = profile_name
        if api_key is not None:
            self.api_key = api_key
        if token is not None:
            self.token = token
        if premium_start_date is not None:
            self.premium_start_date = premium_start_date
        if charging_start_date is not None:
            self.charging_start_date = charging_start_date
        if charging_next_date is not None:
            self.charging_next_date = charging_next_date
        if cancel_date is not None:
            self.cancel_date = cancel_date
        if auth_source is not None:
            self.auth_source = auth_source
        if subscription_id is not None:
            self.subscription_id = subscription_id
        if referer is not None:
            self.referer = referer
        if allow_terminal_logging is not None:
            self.allow_terminal_logging = allow_terminal_logging
        if stripe_customer_id is not None:
            self.stripe_customer_id = stripe_customer_id

    @property
    def user_id(self):
        """Gets the user_id of this UserDto.  # noqa: E501


        :return: The user_id of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this UserDto.


        :param user_id: The user_id of this UserDto.  # noqa: E501
        :type: str
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def first_name(self):
        """Gets the first_name of this UserDto.  # noqa: E501


        :return: The first_name of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this UserDto.


        :param first_name: The first_name of this UserDto.  # noqa: E501
        :type: str
        """

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this UserDto.  # noqa: E501


        :return: The last_name of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this UserDto.


        :param last_name: The last_name of this UserDto.  # noqa: E501
        :type: str
        """

        self._last_name = last_name

    @property
    def email(self):
        """Gets the email of this UserDto.  # noqa: E501


        :return: The email of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserDto.


        :param email: The email of this UserDto.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def roles(self):
        """Gets the roles of this UserDto.  # noqa: E501


        :return: The roles of this UserDto.  # noqa: E501
        :rtype: list[str]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this UserDto.


        :param roles: The roles of this UserDto.  # noqa: E501
        :type: list[str]
        """

        self._roles = roles

    @property
    def opt_for_newsletter(self):
        """Gets the opt_for_newsletter of this UserDto.  # noqa: E501


        :return: The opt_for_newsletter of this UserDto.  # noqa: E501
        :rtype: bool
        """
        return self._opt_for_newsletter

    @opt_for_newsletter.setter
    def opt_for_newsletter(self, opt_for_newsletter):
        """Sets the opt_for_newsletter of this UserDto.


        :param opt_for_newsletter: The opt_for_newsletter of this UserDto.  # noqa: E501
        :type: bool
        """

        self._opt_for_newsletter = opt_for_newsletter

    @property
    def country(self):
        """Gets the country of this UserDto.  # noqa: E501


        :return: The country of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this UserDto.


        :param country: The country of this UserDto.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def email_confirmed(self):
        """Gets the email_confirmed of this UserDto.  # noqa: E501


        :return: The email_confirmed of this UserDto.  # noqa: E501
        :rtype: bool
        """
        return self._email_confirmed

    @email_confirmed.setter
    def email_confirmed(self, email_confirmed):
        """Sets the email_confirmed of this UserDto.


        :param email_confirmed: The email_confirmed of this UserDto.  # noqa: E501
        :type: bool
        """

        self._email_confirmed = email_confirmed

    @property
    def created_time(self):
        """Gets the created_time of this UserDto.  # noqa: E501


        :return: The created_time of this UserDto.  # noqa: E501
        :rtype: int
        """
        return self._created_time

    @created_time.setter
    def created_time(self, created_time):
        """Sets the created_time of this UserDto.


        :param created_time: The created_time of this UserDto.  # noqa: E501
        :type: int
        """

        self._created_time = created_time

    @property
    def last_modified(self):
        """Gets the last_modified of this UserDto.  # noqa: E501


        :return: The last_modified of this UserDto.  # noqa: E501
        :rtype: int
        """
        return self._last_modified

    @last_modified.setter
    def last_modified(self, last_modified):
        """Sets the last_modified of this UserDto.


        :param last_modified: The last_modified of this UserDto.  # noqa: E501
        :type: int
        """

        self._last_modified = last_modified

    @property
    def profile_name(self):
        """Gets the profile_name of this UserDto.  # noqa: E501


        :return: The profile_name of this UserDto.  # noqa: E501
        :rtype: ProfileName
        """
        return self._profile_name

    @profile_name.setter
    def profile_name(self, profile_name):
        """Sets the profile_name of this UserDto.


        :param profile_name: The profile_name of this UserDto.  # noqa: E501
        :type: ProfileName
        """

        self._profile_name = profile_name

    @property
    def api_key(self):
        """Gets the api_key of this UserDto.  # noqa: E501


        :return: The api_key of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        """Sets the api_key of this UserDto.


        :param api_key: The api_key of this UserDto.  # noqa: E501
        :type: str
        """

        self._api_key = api_key

    @property
    def token(self):
        """Gets the token of this UserDto.  # noqa: E501


        :return: The token of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this UserDto.


        :param token: The token of this UserDto.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def premium_start_date(self):
        """Gets the premium_start_date of this UserDto.  # noqa: E501


        :return: The premium_start_date of this UserDto.  # noqa: E501
        :rtype: datetime
        """
        return self._premium_start_date

    @premium_start_date.setter
    def premium_start_date(self, premium_start_date):
        """Sets the premium_start_date of this UserDto.


        :param premium_start_date: The premium_start_date of this UserDto.  # noqa: E501
        :type: datetime
        """

        self._premium_start_date = premium_start_date

    @property
    def charging_start_date(self):
        """Gets the charging_start_date of this UserDto.  # noqa: E501


        :return: The charging_start_date of this UserDto.  # noqa: E501
        :rtype: datetime
        """
        return self._charging_start_date

    @charging_start_date.setter
    def charging_start_date(self, charging_start_date):
        """Sets the charging_start_date of this UserDto.


        :param charging_start_date: The charging_start_date of this UserDto.  # noqa: E501
        :type: datetime
        """

        self._charging_start_date = charging_start_date

    @property
    def charging_next_date(self):
        """Gets the charging_next_date of this UserDto.  # noqa: E501


        :return: The charging_next_date of this UserDto.  # noqa: E501
        :rtype: datetime
        """
        return self._charging_next_date

    @charging_next_date.setter
    def charging_next_date(self, charging_next_date):
        """Sets the charging_next_date of this UserDto.


        :param charging_next_date: The charging_next_date of this UserDto.  # noqa: E501
        :type: datetime
        """

        self._charging_next_date = charging_next_date

    @property
    def cancel_date(self):
        """Gets the cancel_date of this UserDto.  # noqa: E501


        :return: The cancel_date of this UserDto.  # noqa: E501
        :rtype: datetime
        """
        return self._cancel_date

    @cancel_date.setter
    def cancel_date(self, cancel_date):
        """Sets the cancel_date of this UserDto.


        :param cancel_date: The cancel_date of this UserDto.  # noqa: E501
        :type: datetime
        """

        self._cancel_date = cancel_date

    @property
    def auth_source(self):
        """Gets the auth_source of this UserDto.  # noqa: E501


        :return: The auth_source of this UserDto.  # noqa: E501
        :rtype: AuthenticationSource
        """
        return self._auth_source

    @auth_source.setter
    def auth_source(self, auth_source):
        """Sets the auth_source of this UserDto.


        :param auth_source: The auth_source of this UserDto.  # noqa: E501
        :type: AuthenticationSource
        """

        self._auth_source = auth_source

    @property
    def subscription_id(self):
        """Gets the subscription_id of this UserDto.  # noqa: E501


        :return: The subscription_id of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, subscription_id):
        """Sets the subscription_id of this UserDto.


        :param subscription_id: The subscription_id of this UserDto.  # noqa: E501
        :type: str
        """

        self._subscription_id = subscription_id

    @property
    def referer(self):
        """Gets the referer of this UserDto.  # noqa: E501


        :return: The referer of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._referer

    @referer.setter
    def referer(self, referer):
        """Sets the referer of this UserDto.


        :param referer: The referer of this UserDto.  # noqa: E501
        :type: str
        """

        self._referer = referer

    @property
    def allow_terminal_logging(self):
        """Gets the allow_terminal_logging of this UserDto.  # noqa: E501


        :return: The allow_terminal_logging of this UserDto.  # noqa: E501
        :rtype: bool
        """
        return self._allow_terminal_logging

    @allow_terminal_logging.setter
    def allow_terminal_logging(self, allow_terminal_logging):
        """Sets the allow_terminal_logging of this UserDto.


        :param allow_terminal_logging: The allow_terminal_logging of this UserDto.  # noqa: E501
        :type: bool
        """

        self._allow_terminal_logging = allow_terminal_logging

    @property
    def stripe_customer_id(self):
        """Gets the stripe_customer_id of this UserDto.  # noqa: E501


        :return: The stripe_customer_id of this UserDto.  # noqa: E501
        :rtype: str
        """
        return self._stripe_customer_id

    @stripe_customer_id.setter
    def stripe_customer_id(self, stripe_customer_id):
        """Sets the stripe_customer_id of this UserDto.


        :param stripe_customer_id: The stripe_customer_id of this UserDto.  # noqa: E501
        :type: str
        """

        self._stripe_customer_id = stripe_customer_id

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
        if issubclass(UserDto, dict):
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
        if not isinstance(other, UserDto):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
