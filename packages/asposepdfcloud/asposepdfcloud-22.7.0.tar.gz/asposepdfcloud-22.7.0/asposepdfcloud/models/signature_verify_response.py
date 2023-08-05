# coding: utf-8

"""
    Aspose.PDF Cloud API Reference


Copyright (c) 2022 Aspose.PDF Cloud
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



    OpenAPI spec version: 3.0
    
"""


from pprint import pformat
from six import iteritems
import re


class SignatureVerifyResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'code': 'int',
        'status': 'str',
        'valid': 'bool'
    }

    attribute_map = {
        'code': 'Code',
        'status': 'Status',
        'valid': 'Valid'
    }

    def __init__(self, code=None, status=None, valid=None):
        """
        SignatureVerifyResponse - a model defined in Swagger
        """

        self._code = None
        self._status = None
        self._valid = None

        self.code = code
        if status is not None:
          self.status = status
        self.valid = valid

    @property
    def code(self):
        """
        Gets the code of this SignatureVerifyResponse.
        Response status code.

        :return: The code of this SignatureVerifyResponse.
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """
        Sets the code of this SignatureVerifyResponse.
        Response status code.

        :param code: The code of this SignatureVerifyResponse.
        :type: int
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")

        self._code = code

    @property
    def status(self):
        """
        Gets the status of this SignatureVerifyResponse.
        Response status.

        :return: The status of this SignatureVerifyResponse.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this SignatureVerifyResponse.
        Response status.

        :param status: The status of this SignatureVerifyResponse.
        :type: str
        """

        self._status = status

    @property
    def valid(self):
        """
        Gets the valid of this SignatureVerifyResponse.
        True if signature is valid and false if not

        :return: The valid of this SignatureVerifyResponse.
        :rtype: bool
        """
        return self._valid

    @valid.setter
    def valid(self, valid):
        """
        Sets the valid of this SignatureVerifyResponse.
        True if signature is valid and false if not

        :param valid: The valid of this SignatureVerifyResponse.
        :type: bool
        """
        if valid is None:
            raise ValueError("Invalid value for `valid`, must not be `None`")

        self._valid = valid

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
        if not isinstance(other, SignatureVerifyResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
