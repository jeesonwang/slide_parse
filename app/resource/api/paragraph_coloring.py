#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import time
import os
import uuid

from loguru import logger
from flask_restful import Resource
from app.common.response import ResUtil, fields, args_parser

from app.controller.s3fs_file import s3_controller
from app.controller.slide_parse import slide_ctrl
from app.common.log import logger
from config.const import DOWNLOAD_PATH
from app.engine.parse_results import ProcessingResults

class ParagraphColoringResource(Resource, ResUtil):
    @args_parser({
        "filepath": fields(type=str, required=True),
        "pdf_filepath": fields(type=str, required=True),
        "coloring_pdf_filepath": fields(type=str, required=True)
    })
    def post(self, filepath: str, pdf_filepath: str, coloring_pdf_filepath: str):
        if filepath.split(".")[-1] not in ("pptx", "ppt"):
            return self.message(code=1102, message=f"只支持pptx或ppt的文档")
        
        file_name = os.path.basename(filepath)
        # download from s3 to folder
        file_path = os.path.join(DOWNLOAD_PATH, file_name)
        s3_controller.download_file(file_path=filepath, download_path=file_path)

        if not os.path.exists(file_path):
            return self.message(code=1111, message=f"file: [{file_path}] not exist")

        results: ProcessingResults
        results = slide_ctrl.set_paragraph_colors(file_path)
        logger.info(f"原pdf文件: {results.origin_pdf_path}, 染色后的pdf文件: {results.colored_pdf_path}")
        s3_controller.upload(results.origin_pdf_path, pdf_filepath)
        s3_controller.upload(results.colored_pdf_path, coloring_pdf_filepath)
        
        return self.message(data=results.data, message="success")
