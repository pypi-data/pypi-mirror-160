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


class DocumentConfig(object):
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
        'display_properties': 'DisplayProperties',
        'document_properties': 'DocumentProperties',
        'pages_count': 'int',
        'default_page_config': 'DefaultPageConfig'
    }

    attribute_map = {
        'display_properties': 'DisplayProperties',
        'document_properties': 'DocumentProperties',
        'pages_count': 'PagesCount',
        'default_page_config': 'DefaultPageConfig'
    }

    def __init__(self, display_properties=None, document_properties=None, pages_count=None, default_page_config=None):
        """
        DocumentConfig - a model defined in Swagger
        """

        self._display_properties = None
        self._document_properties = None
        self._pages_count = None
        self._default_page_config = None

        if display_properties is not None:
          self.display_properties = display_properties
        if document_properties is not None:
          self.document_properties = document_properties
        self.pages_count = pages_count
        if default_page_config is not None:
          self.default_page_config = default_page_config

    @property
    def display_properties(self):
        """
        Gets the display_properties of this DocumentConfig.
        Sets DisplayProperties of document

        :return: The display_properties of this DocumentConfig.
        :rtype: DisplayProperties
        """
        return self._display_properties

    @display_properties.setter
    def display_properties(self, display_properties):
        """
        Sets the display_properties of this DocumentConfig.
        Sets DisplayProperties of document

        :param display_properties: The display_properties of this DocumentConfig.
        :type: DisplayProperties
        """

        self._display_properties = display_properties

    @property
    def document_properties(self):
        """
        Gets the document_properties of this DocumentConfig.
        Sets DocumentProperties of document

        :return: The document_properties of this DocumentConfig.
        :rtype: DocumentProperties
        """
        return self._document_properties

    @document_properties.setter
    def document_properties(self, document_properties):
        """
        Sets the document_properties of this DocumentConfig.
        Sets DocumentProperties of document

        :param document_properties: The document_properties of this DocumentConfig.
        :type: DocumentProperties
        """

        self._document_properties = document_properties

    @property
    def pages_count(self):
        """
        Gets the pages_count of this DocumentConfig.
        Sets count of pages for new document. From 1 to 100

        :return: The pages_count of this DocumentConfig.
        :rtype: int
        """
        return self._pages_count

    @pages_count.setter
    def pages_count(self, pages_count):
        """
        Sets the pages_count of this DocumentConfig.
        Sets count of pages for new document. From 1 to 100

        :param pages_count: The pages_count of this DocumentConfig.
        :type: int
        """
        if pages_count is None:
            raise ValueError("Invalid value for `pages_count`, must not be `None`")

        self._pages_count = pages_count

    @property
    def default_page_config(self):
        """
        Gets the default_page_config of this DocumentConfig.
        Sets default page config for new document

        :return: The default_page_config of this DocumentConfig.
        :rtype: DefaultPageConfig
        """
        return self._default_page_config

    @default_page_config.setter
    def default_page_config(self, default_page_config):
        """
        Sets the default_page_config of this DocumentConfig.
        Sets default page config for new document

        :param default_page_config: The default_page_config of this DocumentConfig.
        :type: DefaultPageConfig
        """

        self._default_page_config = default_page_config

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
        if not isinstance(other, DocumentConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
