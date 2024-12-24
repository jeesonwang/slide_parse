#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import tempfile

from loguru import logger

from app.engine.aspose_slides import *
from config.const import COLOR_PATH, DOWNLOAD_PATH
from app.controller.color_manager import ColorManager
from app.engine.parse_results import ProcessingResults

class SlideController(object):
    @staticmethod
    def set_paragraph_colors(file_path):
        file_name = os.path.basename(file_path)
        color_manager = ColorManager()
        logger.info(f"【幻灯片解析开始】 :{file_path}")
        origin_pdf_path = slide_convert_pdf(file_path=file_path)

        presentation = get_doc_obj(file_path)
        results_ = dict(title=None, paragraph=[])

        for slide in presentation.getSlides():
            for shape in slide.getShapes():
                slide_ctrl.parse_shape(shape, color_manager, results_)

        file_title = file_name.split('.')[0]
        colored_file_path = os.path.join(COLOR_PATH, file_name)
        presentation.save(colored_file_path, SaveFormat.Ppt)
        presentation.dispose()
        colored_pdf_path = slide_convert_pdf(file_path=colored_file_path, pdf_name=f"{file_title}_coloring")
        results_["title"] = file_title
        
        logger.info(f"【幻灯片解析结束】:{file_path}")

        return ProcessingResults(colored_pdf_path=colored_pdf_path, origin_pdf_path=origin_pdf_path, data=results_)
    
    @staticmethod
    def paragraph_entry(style_name, 
                        content, 
                        color,
                        *, 
                        titles = None, 
                        assist_content = "", 
                        markdown_content = None, 
                        table_detail = None, 
                        fn_results: list = []
                        ):
        if not markdown_content:
            markdown_content = content
        return [{
            "type_": str(style_name).lower(),
            "title": titles if titles else None,
            "content": content,
            "assist": assist_content,
            "markdown_content": markdown_content,
            "color": str(string_color(color)),
            "table_detail": table_detail
        }] + fn_results

    @staticmethod
    def parse_shape(shape, color_manager: ColorManager, results: dict):

        if isinstance(shape, Portion):
            return
        
        content = ""
        color = None
        type_name = None

        if isinstance(shape, AutoShape):
            shape_type = ShapeType.getName(ShapeType, shape.getShapeType())

            for para in shape.getTextFrame().getParagraphs().iterator():
                slide_ctrl.parse_paragraph(para, shape_type, color_manager, results)
            return
        elif isinstance(shape, Cell):
            shape_type = "cell"
            for para in shape.getTextFrame().getParagraphs().iterator():
                slide_ctrl.parse_paragraph(para, shape_type, color_manager, results)
            return
        elif isinstance(shape, GroupShape):
            for sub_shape in shape.getShapes():
                slide_ctrl.parse_shape(sub_shape, color_manager, results)
            return
        elif isinstance(shape, Table):
            slide_ctrl.parse_table(shape, color_manager, results)
            return
        elif isinstance(shape, AudioFrame):
            type_name = "audio"
        elif isinstance(shape, VideoFrame):
            type_name = "video"
        elif isinstance(shape, PictureFrame):
            type_name = "picture"
        elif isinstance(shape, Connector):
            type_name = "connector"

        if type_name:
            results["paragraph"].extend(slide_ctrl.paragraph_entry(type_name, content, color))

    @staticmethod
    def parse_paragraph(para, type_name, color_manager: ColorManager, results: dict):
        if isinstance(para, Paragraph):
            color = None
            content = str(para.getText())
            if content:
                color = slide_ctrl.coloring_paragraph(para, color_manager)
            results["paragraph"].extend(slide_ctrl.paragraph_entry(type_name, content, color))
        else:
            raise ValueError("The in put parameter para must be Paragraph.")

    @staticmethod
    def to_markdown_table(table) -> str:
        row_count = table.getRows().size()
        column_count = table.getRows().get_Item(0).size()
        _table = []
        rows = table.getRows()
        for i in range(rows.size()):
            row = rows.get_Item(i)
            row_element = []
            for j in range(row.size()):
                cell = row.get_Item(j)
                row_element.append(str(cell.getTextFrame().getText()))
            _table.append(row_element)
        assert len(_table) == row_count
        markdown_table = []
        # the first is table header.
        header = _table[0]
        if len(header) < column_count:
            header[1:1] = [''] * (column_count - len(header))
        markdown_table.append("| " + " | ".join(header) + " |")
        markdown_table.append("| " + " | ".join(["---"] * len(header)) + " |")
        for row in _table[1:]:
            if len(row) < column_count:
                row[1:1] = [''] * (column_count - len(row))
            markdown_table.append("| " + " | ".join(row) + " |")
        return "\n".join(markdown_table)

    @staticmethod
    def to_html_table(table) -> str:
        html_table = "<table border=\"1\">"
        for row in table.getRows():
            html_table += "<tr>"
            for cell in row:
                col_span = cell.getColSpan()
                row_span = cell.getRowSpan()
                text = str(cell.getTextFrame().getText()) if cell.getTextFrame() else ""

                html_table += f"<td"
                if col_span > 1:
                    html_table += f" colspan=\"{col_span}\""
                if row_span > 1:
                    html_table += f" rowspan=\"{row_span}\""
                html_table += f">{text}</td>"
            html_table += "</tr>"
        html_table += "</table>"
        return html_table
    
    @staticmethod
    def coloring_paragraph(paragraph, color_manager: ColorManager):
        color = color_manager.get_color()
        for portion in paragraph.getPortions():
            fill_format = portion.getPortionFormat().getFillFormat()
            fill_format.setFillType(FillType.Solid)
            fill_format.getSolidFillColor().setColor(color)
            
        return color
    
    @staticmethod
    def parse_table(table_shape, color_manager: ColorManager, results: dict):
        """
        Processing table shape.
        """
        shape_type = "table"
        assist_content = slide_ctrl.to_html_table(table_shape)
        markdown_content = slide_ctrl.to_markdown_table(table_shape)
        table_detail, table_content = slide_ctrl.parse_table_detail(table_shape, color_manager)
        results["paragraph"].extend(
            slide_ctrl.paragraph_entry(shape_type,
                                        table_content,
                                        color=None, 
                                        assist_content=assist_content,
                                        markdown_content=markdown_content,
                                        table_detail=table_detail)
                                        )

    @staticmethod
    def parse_table_detail(table, color_manager: ColorManager):    
        row_count = table.getRows().size()
        cells = []
        columns = []
        table_detail = {
            "row_num": row_count,
            "columns": columns,
            "cells": cells
            }
        table_content = ""

        rows = table.getRows()
        for i in range(rows.size()):
            row = rows.get_Item(i)
            previous_content = None
            for j in range(row.size()):
                cell = row.get_Item(j)
                # is_mergedcell = cell.isMergedCell()
                col_span = cell.getColSpan()
                row_span = cell.getRowSpan()

                column = set()
                cell_paragraph = dict(title=None, paragraph=[])
                slide_ctrl.parse_shape(cell, color_manager=color_manager, results=cell_paragraph)
                if i == 0:
                    columns.append(str(cell.getTextFrame().getText()))
                    cells.append({
                    "column": [columns[j]],
                    "ColSpan": col_span,
                    "RowSpan": row_span,
                    "Position": [i, j],
                    "paragraph": cell_paragraph["paragraph"]
                    })
                    table_detail["columns"] = columns
                else:
                    if col_span > 1:
                        if previous_content:
                            column = previous_content
                        else:
                            column.update(columns[j:j+col_span])
                            previous_content = column
                    else:
                        column = [columns[j]]
                        previous_content = None

                    cells.append({
                    "column": list(column),
                    "ColSpan": col_span,
                    "RowSpan": row_span,
                    "Position": [i, j],
                    "paragraph": cell_paragraph["paragraph"]
                    })
                table_content += str(cell.getTextFrame().getText())
            table_content += "\n"

        table_detail["cells"] = cells
        return table_detail, table_content


slide_ctrl = SlideController()
