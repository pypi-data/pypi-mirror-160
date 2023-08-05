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


class FileAttachmentAnnotation(object):
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
        'links': 'list[Link]',
        'color': 'Color',
        'contents': 'str',
        'modified': 'str',
        'id': 'str',
        'flags': 'list[AnnotationFlags]',
        'name': 'str',
        'rect': 'Rectangle',
        'page_index': 'int',
        'z_index': 'int',
        'horizontal_alignment': 'HorizontalAlignment',
        'vertical_alignment': 'VerticalAlignment',
        'creation_date': 'str',
        'subject': 'str',
        'title': 'str',
        'rich_text': 'str',
        'icon': 'FileIcon',
        'opacity': 'float',
        'file_description': 'str',
        'file_name': 'str',
        'file_path': 'str'
    }

    attribute_map = {
        'links': 'Links',
        'color': 'Color',
        'contents': 'Contents',
        'modified': 'Modified',
        'id': 'Id',
        'flags': 'Flags',
        'name': 'Name',
        'rect': 'Rect',
        'page_index': 'PageIndex',
        'z_index': 'ZIndex',
        'horizontal_alignment': 'HorizontalAlignment',
        'vertical_alignment': 'VerticalAlignment',
        'creation_date': 'CreationDate',
        'subject': 'Subject',
        'title': 'Title',
        'rich_text': 'RichText',
        'icon': 'Icon',
        'opacity': 'Opacity',
        'file_description': 'FileDescription',
        'file_name': 'FileName',
        'file_path': 'FilePath'
    }

    def __init__(self, links=None, color=None, contents=None, modified=None, id=None, flags=None, name=None, rect=None, page_index=None, z_index=None, horizontal_alignment=None, vertical_alignment=None, creation_date=None, subject=None, title=None, rich_text=None, icon=None, opacity=None, file_description=None, file_name=None, file_path=None):
        """
        FileAttachmentAnnotation - a model defined in Swagger
        """

        self._links = None
        self._color = None
        self._contents = None
        self._modified = None
        self._id = None
        self._flags = None
        self._name = None
        self._rect = None
        self._page_index = None
        self._z_index = None
        self._horizontal_alignment = None
        self._vertical_alignment = None
        self._creation_date = None
        self._subject = None
        self._title = None
        self._rich_text = None
        self._icon = None
        self._opacity = None
        self._file_description = None
        self._file_name = None
        self._file_path = None

        if links is not None:
          self.links = links
        if color is not None:
          self.color = color
        if contents is not None:
          self.contents = contents
        if modified is not None:
          self.modified = modified
        if id is not None:
          self.id = id
        if flags is not None:
          self.flags = flags
        if name is not None:
          self.name = name
        self.rect = rect
        if page_index is not None:
          self.page_index = page_index
        if z_index is not None:
          self.z_index = z_index
        if horizontal_alignment is not None:
          self.horizontal_alignment = horizontal_alignment
        if vertical_alignment is not None:
          self.vertical_alignment = vertical_alignment
        if creation_date is not None:
          self.creation_date = creation_date
        if subject is not None:
          self.subject = subject
        if title is not None:
          self.title = title
        if rich_text is not None:
          self.rich_text = rich_text
        if icon is not None:
          self.icon = icon
        if opacity is not None:
          self.opacity = opacity
        if file_description is not None:
          self.file_description = file_description
        if file_name is not None:
          self.file_name = file_name
        if file_path is not None:
          self.file_path = file_path

    @property
    def links(self):
        """
        Gets the links of this FileAttachmentAnnotation.
        Link to the document.

        :return: The links of this FileAttachmentAnnotation.
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this FileAttachmentAnnotation.
        Link to the document.

        :param links: The links of this FileAttachmentAnnotation.
        :type: list[Link]
        """

        self._links = links

    @property
    def color(self):
        """
        Gets the color of this FileAttachmentAnnotation.
        Color of the annotation.

        :return: The color of this FileAttachmentAnnotation.
        :rtype: Color
        """
        return self._color

    @color.setter
    def color(self, color):
        """
        Sets the color of this FileAttachmentAnnotation.
        Color of the annotation.

        :param color: The color of this FileAttachmentAnnotation.
        :type: Color
        """

        self._color = color

    @property
    def contents(self):
        """
        Gets the contents of this FileAttachmentAnnotation.
        Get the annotation content.

        :return: The contents of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._contents

    @contents.setter
    def contents(self, contents):
        """
        Sets the contents of this FileAttachmentAnnotation.
        Get the annotation content.

        :param contents: The contents of this FileAttachmentAnnotation.
        :type: str
        """

        self._contents = contents

    @property
    def modified(self):
        """
        Gets the modified of this FileAttachmentAnnotation.
        The date and time when the annotation was last modified.

        :return: The modified of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """
        Sets the modified of this FileAttachmentAnnotation.
        The date and time when the annotation was last modified.

        :param modified: The modified of this FileAttachmentAnnotation.
        :type: str
        """

        self._modified = modified

    @property
    def id(self):
        """
        Gets the id of this FileAttachmentAnnotation.
        Gets ID of the annotation.

        :return: The id of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this FileAttachmentAnnotation.
        Gets ID of the annotation.

        :param id: The id of this FileAttachmentAnnotation.
        :type: str
        """

        self._id = id

    @property
    def flags(self):
        """
        Gets the flags of this FileAttachmentAnnotation.
        Gets Flags of the annotation.

        :return: The flags of this FileAttachmentAnnotation.
        :rtype: list[AnnotationFlags]
        """
        return self._flags

    @flags.setter
    def flags(self, flags):
        """
        Sets the flags of this FileAttachmentAnnotation.
        Gets Flags of the annotation.

        :param flags: The flags of this FileAttachmentAnnotation.
        :type: list[AnnotationFlags]
        """

        self._flags = flags

    @property
    def name(self):
        """
        Gets the name of this FileAttachmentAnnotation.
        Gets Name of the annotation.

        :return: The name of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FileAttachmentAnnotation.
        Gets Name of the annotation.

        :param name: The name of this FileAttachmentAnnotation.
        :type: str
        """

        self._name = name

    @property
    def rect(self):
        """
        Gets the rect of this FileAttachmentAnnotation.
        Gets Rect of the annotation.

        :return: The rect of this FileAttachmentAnnotation.
        :rtype: Rectangle
        """
        return self._rect

    @rect.setter
    def rect(self, rect):
        """
        Sets the rect of this FileAttachmentAnnotation.
        Gets Rect of the annotation.

        :param rect: The rect of this FileAttachmentAnnotation.
        :type: Rectangle
        """
        if rect is None:
            raise ValueError("Invalid value for `rect`, must not be `None`")

        self._rect = rect

    @property
    def page_index(self):
        """
        Gets the page_index of this FileAttachmentAnnotation.
        Gets PageIndex of the annotation.

        :return: The page_index of this FileAttachmentAnnotation.
        :rtype: int
        """
        return self._page_index

    @page_index.setter
    def page_index(self, page_index):
        """
        Sets the page_index of this FileAttachmentAnnotation.
        Gets PageIndex of the annotation.

        :param page_index: The page_index of this FileAttachmentAnnotation.
        :type: int
        """

        self._page_index = page_index

    @property
    def z_index(self):
        """
        Gets the z_index of this FileAttachmentAnnotation.
        Gets ZIndex of the annotation.

        :return: The z_index of this FileAttachmentAnnotation.
        :rtype: int
        """
        return self._z_index

    @z_index.setter
    def z_index(self, z_index):
        """
        Sets the z_index of this FileAttachmentAnnotation.
        Gets ZIndex of the annotation.

        :param z_index: The z_index of this FileAttachmentAnnotation.
        :type: int
        """

        self._z_index = z_index

    @property
    def horizontal_alignment(self):
        """
        Gets the horizontal_alignment of this FileAttachmentAnnotation.
        Gets HorizontalAlignment of the annotation.

        :return: The horizontal_alignment of this FileAttachmentAnnotation.
        :rtype: HorizontalAlignment
        """
        return self._horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, horizontal_alignment):
        """
        Sets the horizontal_alignment of this FileAttachmentAnnotation.
        Gets HorizontalAlignment of the annotation.

        :param horizontal_alignment: The horizontal_alignment of this FileAttachmentAnnotation.
        :type: HorizontalAlignment
        """

        self._horizontal_alignment = horizontal_alignment

    @property
    def vertical_alignment(self):
        """
        Gets the vertical_alignment of this FileAttachmentAnnotation.
        Gets VerticalAlignment of the annotation.

        :return: The vertical_alignment of this FileAttachmentAnnotation.
        :rtype: VerticalAlignment
        """
        return self._vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, vertical_alignment):
        """
        Sets the vertical_alignment of this FileAttachmentAnnotation.
        Gets VerticalAlignment of the annotation.

        :param vertical_alignment: The vertical_alignment of this FileAttachmentAnnotation.
        :type: VerticalAlignment
        """

        self._vertical_alignment = vertical_alignment

    @property
    def creation_date(self):
        """
        Gets the creation_date of this FileAttachmentAnnotation.
        The date and time when the annotation was created.

        :return: The creation_date of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        """
        Sets the creation_date of this FileAttachmentAnnotation.
        The date and time when the annotation was created.

        :param creation_date: The creation_date of this FileAttachmentAnnotation.
        :type: str
        """

        self._creation_date = creation_date

    @property
    def subject(self):
        """
        Gets the subject of this FileAttachmentAnnotation.
        Get the annotation subject.

        :return: The subject of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._subject

    @subject.setter
    def subject(self, subject):
        """
        Sets the subject of this FileAttachmentAnnotation.
        Get the annotation subject.

        :param subject: The subject of this FileAttachmentAnnotation.
        :type: str
        """

        self._subject = subject

    @property
    def title(self):
        """
        Gets the title of this FileAttachmentAnnotation.
        Get the annotation title.

        :return: The title of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        Sets the title of this FileAttachmentAnnotation.
        Get the annotation title.

        :param title: The title of this FileAttachmentAnnotation.
        :type: str
        """

        self._title = title

    @property
    def rich_text(self):
        """
        Gets the rich_text of this FileAttachmentAnnotation.
        Get the annotation RichText.

        :return: The rich_text of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._rich_text

    @rich_text.setter
    def rich_text(self, rich_text):
        """
        Sets the rich_text of this FileAttachmentAnnotation.
        Get the annotation RichText.

        :param rich_text: The rich_text of this FileAttachmentAnnotation.
        :type: str
        """

        self._rich_text = rich_text

    @property
    def icon(self):
        """
        Gets the icon of this FileAttachmentAnnotation.
        Gets or sets icon that shall be used in displaying annotation.

        :return: The icon of this FileAttachmentAnnotation.
        :rtype: FileIcon
        """
        return self._icon

    @icon.setter
    def icon(self, icon):
        """
        Sets the icon of this FileAttachmentAnnotation.
        Gets or sets icon that shall be used in displaying annotation.

        :param icon: The icon of this FileAttachmentAnnotation.
        :type: FileIcon
        """

        self._icon = icon

    @property
    def opacity(self):
        """
        Gets the opacity of this FileAttachmentAnnotation.
        Gets or sets icon's opacity from 0 to 1: 0 - completely transparant, 1 - completely opaque.

        :return: The opacity of this FileAttachmentAnnotation.
        :rtype: float
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        """
        Sets the opacity of this FileAttachmentAnnotation.
        Gets or sets icon's opacity from 0 to 1: 0 - completely transparant, 1 - completely opaque.

        :param opacity: The opacity of this FileAttachmentAnnotation.
        :type: float
        """

        self._opacity = opacity

    @property
    def file_description(self):
        """
        Gets the file_description of this FileAttachmentAnnotation.
        Gets or sets text associated with the file specification. 

        :return: The file_description of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._file_description

    @file_description.setter
    def file_description(self, file_description):
        """
        Sets the file_description of this FileAttachmentAnnotation.
        Gets or sets text associated with the file specification. 

        :param file_description: The file_description of this FileAttachmentAnnotation.
        :type: str
        """

        self._file_description = file_description

    @property
    def file_name(self):
        """
        Gets the file_name of this FileAttachmentAnnotation.
        Gets or sets file specification name. 

        :return: The file_name of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name):
        """
        Sets the file_name of this FileAttachmentAnnotation.
        Gets or sets file specification name. 

        :param file_name: The file_name of this FileAttachmentAnnotation.
        :type: str
        """

        self._file_name = file_name

    @property
    def file_path(self):
        """
        Gets the file_path of this FileAttachmentAnnotation.
        Sets content file path. 

        :return: The file_path of this FileAttachmentAnnotation.
        :rtype: str
        """
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        """
        Sets the file_path of this FileAttachmentAnnotation.
        Sets content file path. 

        :param file_path: The file_path of this FileAttachmentAnnotation.
        :type: str
        """

        self._file_path = file_path

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
        if not isinstance(other, FileAttachmentAnnotation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
