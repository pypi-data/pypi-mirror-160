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


class ComboBoxField(object):
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
        'partial_name': 'str',
        'full_name': 'str',
        'rect': 'Rectangle',
        'value': 'str',
        'page_index': 'int',
        'height': 'float',
        'width': 'float',
        'z_index': 'int',
        'is_group': 'bool',
        'parent': 'FormField',
        'is_shared_field': 'bool',
        'flags': 'list[AnnotationFlags]',
        'color': 'Color',
        'contents': 'str',
        'margin': 'MarginInfo',
        'highlighting': 'LinkHighlightingMode',
        'horizontal_alignment': 'HorizontalAlignment',
        'vertical_alignment': 'VerticalAlignment',
        'border': 'Border',
        'multi_select': 'bool',
        'selected': 'int',
        'options': 'list[Option]',
        'active_state': 'str',
        'editable': 'bool',
        'spell_check': 'bool'
    }

    attribute_map = {
        'links': 'Links',
        'partial_name': 'PartialName',
        'full_name': 'FullName',
        'rect': 'Rect',
        'value': 'Value',
        'page_index': 'PageIndex',
        'height': 'Height',
        'width': 'Width',
        'z_index': 'ZIndex',
        'is_group': 'IsGroup',
        'parent': 'Parent',
        'is_shared_field': 'IsSharedField',
        'flags': 'Flags',
        'color': 'Color',
        'contents': 'Contents',
        'margin': 'Margin',
        'highlighting': 'Highlighting',
        'horizontal_alignment': 'HorizontalAlignment',
        'vertical_alignment': 'VerticalAlignment',
        'border': 'Border',
        'multi_select': 'MultiSelect',
        'selected': 'Selected',
        'options': 'Options',
        'active_state': 'ActiveState',
        'editable': 'Editable',
        'spell_check': 'SpellCheck'
    }

    def __init__(self, links=None, partial_name=None, full_name=None, rect=None, value=None, page_index=None, height=None, width=None, z_index=None, is_group=None, parent=None, is_shared_field=None, flags=None, color=None, contents=None, margin=None, highlighting=None, horizontal_alignment=None, vertical_alignment=None, border=None, multi_select=None, selected=None, options=None, active_state=None, editable=None, spell_check=None):
        """
        ComboBoxField - a model defined in Swagger
        """

        self._links = None
        self._partial_name = None
        self._full_name = None
        self._rect = None
        self._value = None
        self._page_index = None
        self._height = None
        self._width = None
        self._z_index = None
        self._is_group = None
        self._parent = None
        self._is_shared_field = None
        self._flags = None
        self._color = None
        self._contents = None
        self._margin = None
        self._highlighting = None
        self._horizontal_alignment = None
        self._vertical_alignment = None
        self._border = None
        self._multi_select = None
        self._selected = None
        self._options = None
        self._active_state = None
        self._editable = None
        self._spell_check = None

        if links is not None:
          self.links = links
        if partial_name is not None:
          self.partial_name = partial_name
        if full_name is not None:
          self.full_name = full_name
        if rect is not None:
          self.rect = rect
        if value is not None:
          self.value = value
        self.page_index = page_index
        if height is not None:
          self.height = height
        if width is not None:
          self.width = width
        if z_index is not None:
          self.z_index = z_index
        if is_group is not None:
          self.is_group = is_group
        if parent is not None:
          self.parent = parent
        if is_shared_field is not None:
          self.is_shared_field = is_shared_field
        if flags is not None:
          self.flags = flags
        if color is not None:
          self.color = color
        if contents is not None:
          self.contents = contents
        if margin is not None:
          self.margin = margin
        if highlighting is not None:
          self.highlighting = highlighting
        if horizontal_alignment is not None:
          self.horizontal_alignment = horizontal_alignment
        if vertical_alignment is not None:
          self.vertical_alignment = vertical_alignment
        if border is not None:
          self.border = border
        if multi_select is not None:
          self.multi_select = multi_select
        if selected is not None:
          self.selected = selected
        if options is not None:
          self.options = options
        if active_state is not None:
          self.active_state = active_state
        if editable is not None:
          self.editable = editable
        if spell_check is not None:
          self.spell_check = spell_check

    @property
    def links(self):
        """
        Gets the links of this ComboBoxField.
        Link to the document.

        :return: The links of this ComboBoxField.
        :rtype: list[Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this ComboBoxField.
        Link to the document.

        :param links: The links of this ComboBoxField.
        :type: list[Link]
        """

        self._links = links

    @property
    def partial_name(self):
        """
        Gets the partial_name of this ComboBoxField.
        Field name.

        :return: The partial_name of this ComboBoxField.
        :rtype: str
        """
        return self._partial_name

    @partial_name.setter
    def partial_name(self, partial_name):
        """
        Sets the partial_name of this ComboBoxField.
        Field name.

        :param partial_name: The partial_name of this ComboBoxField.
        :type: str
        """

        self._partial_name = partial_name

    @property
    def full_name(self):
        """
        Gets the full_name of this ComboBoxField.
        Full Field name.

        :return: The full_name of this ComboBoxField.
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """
        Sets the full_name of this ComboBoxField.
        Full Field name.

        :param full_name: The full_name of this ComboBoxField.
        :type: str
        """

        self._full_name = full_name

    @property
    def rect(self):
        """
        Gets the rect of this ComboBoxField.
        Field rectangle.

        :return: The rect of this ComboBoxField.
        :rtype: Rectangle
        """
        return self._rect

    @rect.setter
    def rect(self, rect):
        """
        Sets the rect of this ComboBoxField.
        Field rectangle.

        :param rect: The rect of this ComboBoxField.
        :type: Rectangle
        """

        self._rect = rect

    @property
    def value(self):
        """
        Gets the value of this ComboBoxField.
        Field value.

        :return: The value of this ComboBoxField.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this ComboBoxField.
        Field value.

        :param value: The value of this ComboBoxField.
        :type: str
        """

        self._value = value

    @property
    def page_index(self):
        """
        Gets the page_index of this ComboBoxField.
        Page index.

        :return: The page_index of this ComboBoxField.
        :rtype: int
        """
        return self._page_index

    @page_index.setter
    def page_index(self, page_index):
        """
        Sets the page_index of this ComboBoxField.
        Page index.

        :param page_index: The page_index of this ComboBoxField.
        :type: int
        """
        if page_index is None:
            raise ValueError("Invalid value for `page_index`, must not be `None`")

        self._page_index = page_index

    @property
    def height(self):
        """
        Gets the height of this ComboBoxField.
        Gets or sets height of the field.

        :return: The height of this ComboBoxField.
        :rtype: float
        """
        return self._height

    @height.setter
    def height(self, height):
        """
        Sets the height of this ComboBoxField.
        Gets or sets height of the field.

        :param height: The height of this ComboBoxField.
        :type: float
        """

        self._height = height

    @property
    def width(self):
        """
        Gets the width of this ComboBoxField.
        Gets or sets width of the field.

        :return: The width of this ComboBoxField.
        :rtype: float
        """
        return self._width

    @width.setter
    def width(self, width):
        """
        Sets the width of this ComboBoxField.
        Gets or sets width of the field.

        :param width: The width of this ComboBoxField.
        :type: float
        """

        self._width = width

    @property
    def z_index(self):
        """
        Gets the z_index of this ComboBoxField.
        Z index.

        :return: The z_index of this ComboBoxField.
        :rtype: int
        """
        return self._z_index

    @z_index.setter
    def z_index(self, z_index):
        """
        Sets the z_index of this ComboBoxField.
        Z index.

        :param z_index: The z_index of this ComboBoxField.
        :type: int
        """

        self._z_index = z_index

    @property
    def is_group(self):
        """
        Gets the is_group of this ComboBoxField.
        Is group.

        :return: The is_group of this ComboBoxField.
        :rtype: bool
        """
        return self._is_group

    @is_group.setter
    def is_group(self, is_group):
        """
        Sets the is_group of this ComboBoxField.
        Is group.

        :param is_group: The is_group of this ComboBoxField.
        :type: bool
        """

        self._is_group = is_group

    @property
    def parent(self):
        """
        Gets the parent of this ComboBoxField.
        Gets field parent.

        :return: The parent of this ComboBoxField.
        :rtype: FormField
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Sets the parent of this ComboBoxField.
        Gets field parent.

        :param parent: The parent of this ComboBoxField.
        :type: FormField
        """

        self._parent = parent

    @property
    def is_shared_field(self):
        """
        Gets the is_shared_field of this ComboBoxField.
        Property for Generator support. Used when field is added to header or footer. If true, this field will created once and it's appearance will be visible on all pages of the document. If false, separated field will be created for every document page.

        :return: The is_shared_field of this ComboBoxField.
        :rtype: bool
        """
        return self._is_shared_field

    @is_shared_field.setter
    def is_shared_field(self, is_shared_field):
        """
        Sets the is_shared_field of this ComboBoxField.
        Property for Generator support. Used when field is added to header or footer. If true, this field will created once and it's appearance will be visible on all pages of the document. If false, separated field will be created for every document page.

        :param is_shared_field: The is_shared_field of this ComboBoxField.
        :type: bool
        """

        self._is_shared_field = is_shared_field

    @property
    def flags(self):
        """
        Gets the flags of this ComboBoxField.
        Gets Flags of the field.

        :return: The flags of this ComboBoxField.
        :rtype: list[AnnotationFlags]
        """
        return self._flags

    @flags.setter
    def flags(self, flags):
        """
        Sets the flags of this ComboBoxField.
        Gets Flags of the field.

        :param flags: The flags of this ComboBoxField.
        :type: list[AnnotationFlags]
        """

        self._flags = flags

    @property
    def color(self):
        """
        Gets the color of this ComboBoxField.
        Color of the annotation.

        :return: The color of this ComboBoxField.
        :rtype: Color
        """
        return self._color

    @color.setter
    def color(self, color):
        """
        Sets the color of this ComboBoxField.
        Color of the annotation.

        :param color: The color of this ComboBoxField.
        :type: Color
        """

        self._color = color

    @property
    def contents(self):
        """
        Gets the contents of this ComboBoxField.
        Get the field content.

        :return: The contents of this ComboBoxField.
        :rtype: str
        """
        return self._contents

    @contents.setter
    def contents(self, contents):
        """
        Sets the contents of this ComboBoxField.
        Get the field content.

        :param contents: The contents of this ComboBoxField.
        :type: str
        """

        self._contents = contents

    @property
    def margin(self):
        """
        Gets the margin of this ComboBoxField.
        Gets or sets a outer margin for paragraph (for pdf generation)

        :return: The margin of this ComboBoxField.
        :rtype: MarginInfo
        """
        return self._margin

    @margin.setter
    def margin(self, margin):
        """
        Sets the margin of this ComboBoxField.
        Gets or sets a outer margin for paragraph (for pdf generation)

        :param margin: The margin of this ComboBoxField.
        :type: MarginInfo
        """

        self._margin = margin

    @property
    def highlighting(self):
        """
        Gets the highlighting of this ComboBoxField.
        Field highlighting mode.

        :return: The highlighting of this ComboBoxField.
        :rtype: LinkHighlightingMode
        """
        return self._highlighting

    @highlighting.setter
    def highlighting(self, highlighting):
        """
        Sets the highlighting of this ComboBoxField.
        Field highlighting mode.

        :param highlighting: The highlighting of this ComboBoxField.
        :type: LinkHighlightingMode
        """

        self._highlighting = highlighting

    @property
    def horizontal_alignment(self):
        """
        Gets the horizontal_alignment of this ComboBoxField.
        Gets HorizontalAlignment of the field.

        :return: The horizontal_alignment of this ComboBoxField.
        :rtype: HorizontalAlignment
        """
        return self._horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, horizontal_alignment):
        """
        Sets the horizontal_alignment of this ComboBoxField.
        Gets HorizontalAlignment of the field.

        :param horizontal_alignment: The horizontal_alignment of this ComboBoxField.
        :type: HorizontalAlignment
        """

        self._horizontal_alignment = horizontal_alignment

    @property
    def vertical_alignment(self):
        """
        Gets the vertical_alignment of this ComboBoxField.
        Gets VerticalAlignment of the field.

        :return: The vertical_alignment of this ComboBoxField.
        :rtype: VerticalAlignment
        """
        return self._vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, vertical_alignment):
        """
        Sets the vertical_alignment of this ComboBoxField.
        Gets VerticalAlignment of the field.

        :param vertical_alignment: The vertical_alignment of this ComboBoxField.
        :type: VerticalAlignment
        """

        self._vertical_alignment = vertical_alignment

    @property
    def border(self):
        """
        Gets the border of this ComboBoxField.
        Gets or sets annotation border characteristics.

        :return: The border of this ComboBoxField.
        :rtype: Border
        """
        return self._border

    @border.setter
    def border(self, border):
        """
        Sets the border of this ComboBoxField.
        Gets or sets annotation border characteristics.

        :param border: The border of this ComboBoxField.
        :type: Border
        """

        self._border = border

    @property
    def multi_select(self):
        """
        Gets the multi_select of this ComboBoxField.
        Gets or sets multiselection flag.

        :return: The multi_select of this ComboBoxField.
        :rtype: bool
        """
        return self._multi_select

    @multi_select.setter
    def multi_select(self, multi_select):
        """
        Sets the multi_select of this ComboBoxField.
        Gets or sets multiselection flag.

        :param multi_select: The multi_select of this ComboBoxField.
        :type: bool
        """

        self._multi_select = multi_select

    @property
    def selected(self):
        """
        Gets the selected of this ComboBoxField.
        Gets or sets index of selected item. Numbering of items is started from 1.

        :return: The selected of this ComboBoxField.
        :rtype: int
        """
        return self._selected

    @selected.setter
    def selected(self, selected):
        """
        Sets the selected of this ComboBoxField.
        Gets or sets index of selected item. Numbering of items is started from 1.

        :param selected: The selected of this ComboBoxField.
        :type: int
        """

        self._selected = selected

    @property
    def options(self):
        """
        Gets the options of this ComboBoxField.
        Gets collection of options of the combobox.

        :return: The options of this ComboBoxField.
        :rtype: list[Option]
        """
        return self._options

    @options.setter
    def options(self, options):
        """
        Sets the options of this ComboBoxField.
        Gets collection of options of the combobox.

        :param options: The options of this ComboBoxField.
        :type: list[Option]
        """

        self._options = options

    @property
    def active_state(self):
        """
        Gets the active_state of this ComboBoxField.
        Gets or sets current annotation appearance state.

        :return: The active_state of this ComboBoxField.
        :rtype: str
        """
        return self._active_state

    @active_state.setter
    def active_state(self, active_state):
        """
        Sets the active_state of this ComboBoxField.
        Gets or sets current annotation appearance state.

        :param active_state: The active_state of this ComboBoxField.
        :type: str
        """

        self._active_state = active_state

    @property
    def editable(self):
        """
        Gets the editable of this ComboBoxField.
        Gets or sets editable status of the field.

        :return: The editable of this ComboBoxField.
        :rtype: bool
        """
        return self._editable

    @editable.setter
    def editable(self, editable):
        """
        Sets the editable of this ComboBoxField.
        Gets or sets editable status of the field.

        :param editable: The editable of this ComboBoxField.
        :type: bool
        """

        self._editable = editable

    @property
    def spell_check(self):
        """
        Gets the spell_check of this ComboBoxField.
        Gets or sets spellchaeck activiity status.

        :return: The spell_check of this ComboBoxField.
        :rtype: bool
        """
        return self._spell_check

    @spell_check.setter
    def spell_check(self, spell_check):
        """
        Sets the spell_check of this ComboBoxField.
        Gets or sets spellchaeck activiity status.

        :param spell_check: The spell_check of this ComboBoxField.
        :type: bool
        """

        self._spell_check = spell_check

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
        if not isinstance(other, ComboBoxField):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
