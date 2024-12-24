import os
import re
import uuid
import base64
import shutil
import jpype
from jpype import JClass, JString, JArray
from loguru import logger

from config.const import DOWNLOAD_PATH
from config.conf import BASE_DIR

# jpype.startJVM(r"-Djava.class.path=jar/aspose-slides-19.6.jar")
# jpype.startJVM(r"-Djava.class.path=jar/aspose-slides-20.4-jdk16-c.jar")
jpype.startJVM(r"-Djava.class.path=jar/aspose-slides-22.2-jdk16.jar")

License = JClass('com.aspose.slides.License')
Slide = JClass('com.aspose.slides.Slide')
Audio = JClass('com.aspose.slides.Audio')
Chart = JClass('com.aspose.slides.Chart')
Camera = JClass('com.aspose.slides.Camera')
ChartType = JClass('com.aspose.slides.ChartType')
Background = JClass('com.aspose.slides.Background')
Presentation = JClass('com.aspose.slides.Presentation')
ShapeType = JClass('com.aspose.slides.ShapeType')
Shape = JClass('com.aspose.slides.Shape')
PptOptions = JClass('com.aspose.slides.PptOptions')
Picture = JClass('com.aspose.slides.Picture')
ParagraphFormat = JClass('com.aspose.slides.ParagraphFormat')
PresentationFactory = JClass('com.aspose.slides.PresentationFactory')
Video = JClass('com.aspose.slides.Video')
Table = JClass('com.aspose.slides.Table')
Row = JClass('com.aspose.slides.Row')
Cell = JClass('com.aspose.slides.Cell')
AudioPlayModePreset = JClass('com.aspose.slides.AudioPlayModePreset')
Section = JClass('com.aspose.slides.Section')
Paragraph = JClass('com.aspose.slides.Paragraph')
Portion = JClass('com.aspose.slides.Portion')
SaveFormat = JClass('com.aspose.slides.SaveFormat')
EmbedFontCharacters = JClass('com.aspose.slides.EmbedFontCharacters')
FontSources = JClass('com.aspose.slides.FontSources')
AutoShape = JClass('com.aspose.slides.AutoShape')
Placeholder = JClass('com.aspose.slides.Placeholder')
PlaceholderType = JClass('com.aspose.slides.PlaceholderType')
FillType = JClass('com.aspose.slides.FillType')
GroupShape = JClass('com.aspose.slides.GroupShape')
Connector = JClass('com.aspose.slides.Connector')
AudioFrame = JClass('com.aspose.slides.AudioFrame')
PictureFrame = JClass('com.aspose.slides.PictureFrame')
VideoFrame = JClass('com.aspose.slides.VideoFrame')
FontsLoader = JClass('com.aspose.slides.FontsLoader')
FontData = JClass('com.aspose.slides.FontData')
LoadOptions = JClass('com.aspose.slides.LoadOptions')
PdfOptions = JClass('com.aspose.slides.PdfOptions')
# LoadOptions = JClass('com.aspose.slides.LoadOptions')

ByteArrayInputStream = JClass('java.io.ByteArrayInputStream')
InputStream = JClass('java.io.InputStream')
File = JClass('java.io.File')
Date = JClass('java.util.Date')
FileInputStream = JClass('java.io.FileInputStream')
Color = JClass('java.awt.Color')
Integer = JClass('java.lang.Integer')
FileOutputStream = JClass('java.io.FileOutputStream')
Base64 = JClass('java.util.Base64')
JavaStr = JClass("java.lang.String")
JBoolean = jpype.JClass('java.lang.Boolean')

def string_color(color):
    """
    java颜色对象转字符串
    :param color: java.awt.Color
    :return:
    """
    if not color:
        return color
    rgb = color.getRGB()
    hex_value = hex(rgb & 0xffffff)[2:]
    hex_value = hex_value.zfill(6)
    hex_color = "#" + hex_value
    return hex_color

def get_license():
    result = False
    try:
        license_xml = """<License>
  <Data>
    <Products>
      <Product>Aspose.Total for Java</Product>
      <Product>Aspose.Words for Java</Product>
    </Products>
    <EditionType>Enterprise</EditionType>
    <SubscriptionExpiry>20991231</SubscriptionExpiry>
    <LicenseExpiry>20991231</LicenseExpiry>
    <SerialNumber>8bfe198c-7f0c-4ef8-8ff0-acc3237bf0d7</SerialNumber>
  </Data>
  <Signature>111</Signature>
</License>"""
        license_file = ByteArrayInputStream(JavaStr(license_xml).getBytes("UTF-8"))
        aspose_lic = License()
        aspose_lic.setLicense(license_file)
        
        result = True
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    
    return result

if get_license():
    logger.info("成功认证！")

def get_doc_obj(file_path):
    file = File(file_path)
    input_stream = FileInputStream(file)
    load_options = LoadOptions()
    # load_options.setDefaultRegularFont("Wingdings")
    # load_options.setDefaultAsianFont("Wingdings")
    doc = Presentation(input_stream, load_options)

    return doc

def slide_convert_pdf(file_path, pdf_name = None):
    fonts_path = os.path.join(BASE_DIR, "fonts")
    pres = get_doc_obj(file_path)
    font_folders = JArray(JavaStr)([fonts_path])
    # font_sources = FontSources()
    # font_sources.setFontFolders(font_folders)
    FontsLoader.loadExternalFonts(font_folders)
    pdf_opts = PdfOptions()
    pdf_opts.setDefaultRegularFont("Times New Roman")
    if not pdf_name:
        pdf_name = os.path.basename(file_path)
    pdf_name = pdf_name.split(".")[0] + ".pdf"
    pdf_dir = os.path.join(DOWNLOAD_PATH, 'pdf')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, pdf_name)
    try:
        pres.save(pdf_path, SaveFormat.Pdf, pdf_opts)
    finally:
        if pres != None:  
            pres.dispose()
        # Clears Font Cachce
        FontsLoader.clearCache()
    return pdf_path