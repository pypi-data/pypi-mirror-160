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


from __future__ import absolute_import

# import models into model package
from .annotation_flags import AnnotationFlags
from .annotation_state import AnnotationState
from .annotation_type import AnnotationType
from .antialiasing_processing_type import AntialiasingProcessingType
from .aspose_response import AsposeResponse
from .border import Border
from .border_corner_style import BorderCornerStyle
from .border_effect import BorderEffect
from .border_info import BorderInfo
from .border_style import BorderStyle
from .box_style import BoxStyle
from .cap_style import CapStyle
from .caption_position import CaptionPosition
from .caret_symbol import CaretSymbol
from .cell import Cell
from .cell_recognized import CellRecognized
from .color import Color
from .color_depth import ColorDepth
from .column_adjustment import ColumnAdjustment
from .compression_type import CompressionType
from .crypto_algorithm import CryptoAlgorithm
from .dash import Dash
from .default_page_config import DefaultPageConfig
from .direction import Direction
from .disc_usage import DiscUsage
from .doc_format import DocFormat
from .doc_mdp_access_permission_type import DocMDPAccessPermissionType
from .doc_recognition_mode import DocRecognitionMode
from .document_config import DocumentConfig
from .document_privilege import DocumentPrivilege
from .epub_recognition_mode import EpubRecognitionMode
from .error import Error
from .error_details import ErrorDetails
from .field_type import FieldType
from .file_icon import FileIcon
from .file_versions import FileVersions
from .files_list import FilesList
from .files_upload_result import FilesUploadResult
from .font_encoding_rules import FontEncodingRules
from .font_saving_modes import FontSavingModes
from .font_styles import FontStyles
from .free_text_intent import FreeTextIntent
from .graph_info import GraphInfo
from .horizontal_alignment import HorizontalAlignment
from .html_document_type import HtmlDocumentType
from .html_markup_generation_modes import HtmlMarkupGenerationModes
from .image_compression_version import ImageCompressionVersion
from .image_encoding import ImageEncoding
from .image_fragment import ImageFragment
from .image_src_type import ImageSrcType
from .image_template import ImageTemplate
from .image_templates_request import ImageTemplatesRequest
from .justification import Justification
from .letters_positioning_methods import LettersPositioningMethods
from .line_ending import LineEnding
from .line_intent import LineIntent
from .line_spacing import LineSpacing
from .link import Link
from .link_action_type import LinkActionType
from .link_element import LinkElement
from .link_highlighting_mode import LinkHighlightingMode
from .margin_info import MarginInfo
from .merge_documents import MergeDocuments
from .object_exist import ObjectExist
from .optimize_options import OptimizeOptions
from .option import Option
from .output_format import OutputFormat
from .page_layout import PageLayout
from .page_mode import PageMode
from .page_word_count import PageWordCount
from .paragraph import Paragraph
from .parts_embedding_modes import PartsEmbeddingModes
from .pdf_a_type import PdfAType
from .permissions_flags import PermissionsFlags
from .point import Point
from .poly_intent import PolyIntent
from .position import Position
from .raster_images_saving_modes import RasterImagesSavingModes
from .rectangle import Rectangle
from .rotation import Rotation
from .row import Row
from .row_recognized import RowRecognized
from .segment import Segment
from .shape_type import ShapeType
from .signature import Signature
from .signature_custom_appearance import SignatureCustomAppearance
from .signature_type import SignatureType
from .sound_encoding import SoundEncoding
from .sound_icon import SoundIcon
from .split_result import SplitResult
from .stamp import Stamp
from .stamp_icon import StampIcon
from .stamp_type import StampType
from .storage_exist import StorageExist
from .storage_file import StorageFile
from .table_broken import TableBroken
from .text_horizontal_alignment import TextHorizontalAlignment
from .text_icon import TextIcon
from .text_line import TextLine
from .text_rect import TextRect
from .text_rects import TextRects
from .text_replace import TextReplace
from .text_replace_list_request import TextReplaceListRequest
from .text_state import TextState
from .text_style import TextStyle
from .timestamp_settings import TimestampSettings
from .vertical_alignment import VerticalAlignment
from .word_count import WordCount
from .wrap_mode import WrapMode
from .annotation import Annotation
from .annotations_info import AnnotationsInfo
from .annotations_info_response import AnnotationsInfoResponse
from .attachment import Attachment
from .attachment_response import AttachmentResponse
from .attachments import Attachments
from .attachments_response import AttachmentsResponse
from .bookmark import Bookmark
from .bookmark_response import BookmarkResponse
from .bookmarks import Bookmarks
from .bookmarks_response import BookmarksResponse
from .caret_annotation_response import CaretAnnotationResponse
from .caret_annotations import CaretAnnotations
from .caret_annotations_response import CaretAnnotationsResponse
from .check_box_field_response import CheckBoxFieldResponse
from .check_box_fields import CheckBoxFields
from .check_box_fields_response import CheckBoxFieldsResponse
from .circle_annotation_response import CircleAnnotationResponse
from .circle_annotations import CircleAnnotations
from .circle_annotations_response import CircleAnnotationsResponse
from .combo_box_field_response import ComboBoxFieldResponse
from .combo_box_fields import ComboBoxFields
from .combo_box_fields_response import ComboBoxFieldsResponse
from .display_properties import DisplayProperties
from .display_properties_response import DisplayPropertiesResponse
from .document import Document
from .document_page_response import DocumentPageResponse
from .document_pages_response import DocumentPagesResponse
from .document_properties import DocumentProperties
from .document_properties_response import DocumentPropertiesResponse
from .document_property import DocumentProperty
from .document_property_response import DocumentPropertyResponse
from .document_response import DocumentResponse
from .field import Field
from .field_response import FieldResponse
from .fields import Fields
from .fields_response import FieldsResponse
from .file_attachment_annotation_response import FileAttachmentAnnotationResponse
from .file_attachment_annotations import FileAttachmentAnnotations
from .file_attachment_annotations_response import FileAttachmentAnnotationsResponse
from .file_version import FileVersion
from .form_field import FormField
from .free_text_annotation_response import FreeTextAnnotationResponse
from .free_text_annotations import FreeTextAnnotations
from .free_text_annotations_response import FreeTextAnnotationsResponse
from .highlight_annotation_response import HighlightAnnotationResponse
from .highlight_annotations import HighlightAnnotations
from .highlight_annotations_response import HighlightAnnotationsResponse
from .image import Image
from .image_response import ImageResponse
from .images import Images
from .images_response import ImagesResponse
from .ink_annotation_response import InkAnnotationResponse
from .ink_annotations import InkAnnotations
from .ink_annotations_response import InkAnnotationsResponse
from .line_annotation_response import LineAnnotationResponse
from .line_annotations import LineAnnotations
from .line_annotations_response import LineAnnotationsResponse
from .link_annotation import LinkAnnotation
from .link_annotation_response import LinkAnnotationResponse
from .link_annotations import LinkAnnotations
from .link_annotations_response import LinkAnnotationsResponse
from .list_box_field_response import ListBoxFieldResponse
from .list_box_fields import ListBoxFields
from .list_box_fields_response import ListBoxFieldsResponse
from .movie_annotation_response import MovieAnnotationResponse
from .movie_annotations import MovieAnnotations
from .movie_annotations_response import MovieAnnotationsResponse
from .page import Page
from .pages import Pages
from .poly_line_annotation_response import PolyLineAnnotationResponse
from .poly_line_annotations import PolyLineAnnotations
from .poly_line_annotations_response import PolyLineAnnotationsResponse
from .polygon_annotation_response import PolygonAnnotationResponse
from .polygon_annotations import PolygonAnnotations
from .polygon_annotations_response import PolygonAnnotationsResponse
from .popup_annotation_response import PopupAnnotationResponse
from .popup_annotations import PopupAnnotations
from .popup_annotations_response import PopupAnnotationsResponse
from .radio_button_field_response import RadioButtonFieldResponse
from .radio_button_fields import RadioButtonFields
from .radio_button_fields_response import RadioButtonFieldsResponse
from .redaction_annotation_response import RedactionAnnotationResponse
from .redaction_annotations import RedactionAnnotations
from .redaction_annotations_response import RedactionAnnotationsResponse
from .screen_annotation_response import ScreenAnnotationResponse
from .screen_annotations import ScreenAnnotations
from .screen_annotations_response import ScreenAnnotationsResponse
from .signature_field_response import SignatureFieldResponse
from .signature_fields import SignatureFields
from .signature_fields_response import SignatureFieldsResponse
from .signature_verify_response import SignatureVerifyResponse
from .sound_annotation_response import SoundAnnotationResponse
from .sound_annotations import SoundAnnotations
from .sound_annotations_response import SoundAnnotationsResponse
from .split_result_document import SplitResultDocument
from .split_result_response import SplitResultResponse
from .square_annotation_response import SquareAnnotationResponse
from .square_annotations import SquareAnnotations
from .square_annotations_response import SquareAnnotationsResponse
from .squiggly_annotation_response import SquigglyAnnotationResponse
from .squiggly_annotations import SquigglyAnnotations
from .squiggly_annotations_response import SquigglyAnnotationsResponse
from .stamp_annotation_response import StampAnnotationResponse
from .stamp_annotations import StampAnnotations
from .stamp_annotations_response import StampAnnotationsResponse
from .stamp_base import StampBase
from .stamp_info import StampInfo
from .stamps_info import StampsInfo
from .stamps_info_response import StampsInfoResponse
from .strike_out_annotation_response import StrikeOutAnnotationResponse
from .strike_out_annotations import StrikeOutAnnotations
from .strike_out_annotations_response import StrikeOutAnnotationsResponse
from .table import Table
from .table_recognized import TableRecognized
from .table_recognized_response import TableRecognizedResponse
from .tables_recognized import TablesRecognized
from .tables_recognized_response import TablesRecognizedResponse
from .text_annotation_response import TextAnnotationResponse
from .text_annotations import TextAnnotations
from .text_annotations_response import TextAnnotationsResponse
from .text_box_field_response import TextBoxFieldResponse
from .text_box_fields import TextBoxFields
from .text_box_fields_response import TextBoxFieldsResponse
from .text_rects_response import TextRectsResponse
from .text_replace_response import TextReplaceResponse
from .underline_annotation_response import UnderlineAnnotationResponse
from .underline_annotations import UnderlineAnnotations
from .underline_annotations_response import UnderlineAnnotationsResponse
from .word_count_response import WordCountResponse
from .annotation_info import AnnotationInfo
from .check_box_field import CheckBoxField
from .choice_field import ChoiceField
from .image_footer import ImageFooter
from .image_header import ImageHeader
from .image_stamp import ImageStamp
from .markup_annotation import MarkupAnnotation
from .movie_annotation import MovieAnnotation
from .page_number_stamp import PageNumberStamp
from .pdf_page_stamp import PdfPageStamp
from .popup_annotation import PopupAnnotation
from .radio_button_option_field import RadioButtonOptionField
from .redaction_annotation import RedactionAnnotation
from .screen_annotation import ScreenAnnotation
from .signature_field import SignatureField
from .text_box_field import TextBoxField
from .text_footer import TextFooter
from .text_header import TextHeader
from .text_stamp import TextStamp
from .caret_annotation import CaretAnnotation
from .combo_box_field import ComboBoxField
from .common_figure_annotation import CommonFigureAnnotation
from .file_attachment_annotation import FileAttachmentAnnotation
from .free_text_annotation import FreeTextAnnotation
from .highlight_annotation import HighlightAnnotation
from .ink_annotation import InkAnnotation
from .line_annotation import LineAnnotation
from .list_box_field import ListBoxField
from .poly_annotation import PolyAnnotation
from .popup_annotation_with_parent import PopupAnnotationWithParent
from .radio_button_field import RadioButtonField
from .sound_annotation import SoundAnnotation
from .squiggly_annotation import SquigglyAnnotation
from .stamp_annotation import StampAnnotation
from .strike_out_annotation import StrikeOutAnnotation
from .text_annotation import TextAnnotation
from .underline_annotation import UnderlineAnnotation
from .circle_annotation import CircleAnnotation
from .poly_line_annotation import PolyLineAnnotation
from .polygon_annotation import PolygonAnnotation
from .square_annotation import SquareAnnotation
