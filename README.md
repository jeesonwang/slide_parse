# Slide Parse

## 接口输入参数：

filepath：输入的s3中的word文件路径；

pdf_filepath：输出的未染色的pdf文件存储路径；

coloring_pdf_filepath：输出的染色后的pdf文件存储路径。



### 请求示例：

```shell
curl --location 'http://127.0.0.1:5000/paragraph_coloring' \

--header 'Content-Type: application/json' \

--data '{

​	"filepath": "example-bucket/upload/0/1feca742172a.pptx",

​	"pdf_filepath":"example-bucket/upload/0/1feca742172a.pdf",

​	"coloring_pdf_filepath": "example-bucket/upload/0/1feca742172a_coloring.pdf"

​	}'

```



### 输出响应示例：

```json
{
    "title": "表格测试",
    "paragraph": [
        {
            "type_": "notdefined",
            "title": null,
            "content": "第一页",
            "assist": "",
            "markdown_content": "第一页",
            "color": "#551979",
            "table_detail": null
        },
        {
            "type_": "rectangle",
            "title": null,
            "content": "机器翻译（MT）领域随着Transformer架构的成功而迅速发展。与传统的统计机器翻译相比，基于神经网络的MT能够产生更多样化的句子。",
            "assist": "",
            "markdown_content": "机器翻译（MT）领域随着Transformer架构的成功而迅速发展。与传统的统计机器翻译相比，基于神经网络的MT能够产生更多样化的句子。",
            "color": "#b33c47",
            "table_detail": null
        },
        {
            "type_": "table",
            "title": null,
            "content": "表格1横向合并3，4列横向合并3，4列\n这是一个纵向合并单元格。asg q\r sdf wgh3tg \n这是一个纵向合并单元格。asdf w easdg \n",
            "assist": "<table border=\"1\"><tr><td>表格</td><td>1</td><td colspan=\"2\">横向合并3，4列</td></tr><tr><td rowspan=\"2\">这是一个纵向合并单元格。</td><td>asg q\r</td><td> sdf wgh</td><td>3tg </td></tr><tr><td>asdf </td><td>w e</td><td>asdg </td></tr></table>",
            "markdown_content": "| 表格 | 1 | 横向合并3，4列 | 横向合并3，4列 |\n| --- | --- | --- | --- |\n| 这是一个纵向合并单元格。 | asg q\r |  sdf wgh | 3tg  |\n| 这是一个纵向合并单元格。 | asdf  | w e | asdg  |",
            "color": "None",
            "table_detail": {
                "row_num": 3,  // 表格行数
                "columns": [
                    "表格",
                    "1",
                    "横向合并3，4列",
                    "横向合并3，4列"
                ],   // 表格列名
                "cells": [
                    {
                        "column": [
                            "表格"
                        ],
                        "ColSpan": 1,   // 当前单元格合并的列数
                        "RowSpan": 1,   // 当前单元格合并的行数
                        "Position": [
                            0,
                            0
                        ],
                        "paragraph": [
                            {
                                "type_": "cell",
                                "title": null,
                                "content": "表格",
                                "assist": "",
                                "markdown_content": "表格",
                                "color": "#95513c",
                                "table_detail": null
                            }
                        ]
                    },
                    {
                        "column": [
                            "1"
                        ],
                        "ColSpan": 1,
                        "RowSpan": 1,
                        "Position": [
                            0,
                            1
                        ],
                        "paragraph": [
                            {
                                "type_": "cell",
                                "title": null,
                                "content": "1",
                                "assist": "",
                                "markdown_content": "1",
                                "color": "#9d29d0",
                                "table_detail": null
                            }
                        ]
                    },
                    {
                        "column": [
                            "横向合并3，4列"
                        ],
                        "ColSpan": 2,
                        "RowSpan": 1,
                        "Position": [
                            0,
                            2
                        ],
                        "paragraph": [
                            {
                                "type_": "cell",
                                "title": null,
                                "content": "横向合并3，4列",
                                "assist": "",
                                "markdown_content": "横向合并3，4列",
                                "color": "#11fa58",
                                "table_detail": null
                            }
                        ]
                    },
                    {
                        "column": [
                            "横向合并3，4列"
                        ],
                        "ColSpan": 2,
                        "RowSpan": 1,
                        "Position": [
                            0,
                            3
                        ],
                        "paragraph": [
                            {
                                "type_": "cell",
                                "title": null,
                                "content": "横向合并3，4列",
                                "assist": "",
                                "markdown_content": "横向合并3，4列",
                                "color": "#b94066",
                                "table_detail": null
                            }
                        ]
                    },
                    {
                        "column": [
                            "表格"
                        ],
                        "ColSpan": 1,
                        "RowSpan": 2,
                        "Position": [
                            1,
                            0
                        ],
                        "paragraph": [
                            {
                                "type_": "cell",
                                "title": null,
                                "content": "这是一个纵向合并单元格。",
                                "assist": "",
                                "markdown_content": "这是一个纵向合并单元格。",
                                "color": "#ac735b",
                                "table_detail": null
                            }
                        ]
                    },
                    ...
```
