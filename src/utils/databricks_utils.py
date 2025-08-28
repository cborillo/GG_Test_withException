from __future__ import annotations

import os
from io import BytesIO

from werkzeug.datastructures import FileStorage

from .model_utils import DictComparator


def toggle_dbfs_format(path: str) -> str:
    return (
        path.replace("/dbfs", "dbfs:")
        if "/dbfs" in path
        else path.replace("dbfs:", "/dbfs")
    )


def get_file_storage_from_dbfs(file_path: str) -> FileStorage:
    with open(file_path, "rb") as f:
        file_content = f.read()
    return FileStorage(
        stream=BytesIO(file_content),
        filename=os.path.basename(file_path),
        content_type="image/jpeg",
    )


class DatabricksDictComparator(DictComparator):
    def __init__(self, reference: dict, other: dict) -> None:
        super().__init__(reference, other)

    def to_html(self) -> str:
        comments = {}

        for change_type, changes in self.diff.items():
            for change in changes:
                path = change.path(output_format="list")
                if change_type == "values_changed":
                    comment = (
                        f" <span class='changed'># changed from `{change.t1}`</span>"
                    )
                elif change_type == "type_changes":
                    comment = f" <span class='changed'># type changed from `{change.t1}`</span>"
                elif change_type == "iterable_item_added":
                    comment = " <span class='added'># added</span>"
                elif change_type == "iterable_item_removed":
                    comment = f" <span class='removed'># removed: `{change.t1}`</span>"
                elif change_type == "dictionary_item_added":
                    comment = " <span class='added'># added</span>"
                elif change_type == "dictionary_item_removed":
                    comment = f" <span class='removed'># removed: `{change.t1}`</span>"
                else:
                    comment = f" <span class='changed'># {change_type.replace('_', ' ').capitalize()}: {change}</span>"

                current_dict = comments
                for key in path[:-1]:
                    if key not in current_dict:
                        current_dict[key] = {}
                    current_dict = current_dict[key]
                current_dict[path[-1]] = comment

        commented_data = self._add_comments(self.other, comments)
        html_str = "\n".join(self._dict_to_html(commented_data))
        return f"""
        <style>
            .changed {{ background-color: #fee2e2; color: #b91c1c; }}
            .removed {{ background-color: #ffedd5; color: #c2410c; }}
            .added {{ background-color: #dbeafe; color: #1d4ed8; }}
            pre {{
            font-family: 'Courier New', Courier, monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1;
            }}
        </style>
        <pre>{html_str}</pre>
        """

    def _add_comments(self, data, comments: dict[str]):
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if key in comments:
                    comment = comments[key]
                    if isinstance(comment, str):
                        result[key] = f"{value}{comment}"
                    elif isinstance(comment, dict):
                        result[key] = self._add_comments(value, comment)
                else:
                    result[key] = value
            return result
        if isinstance(data, (list, tuple, set)):
            result = []
            for i, item in enumerate(data):
                if i in comments:
                    comment = comments[i]
                    if isinstance(comment, str):
                        result.append(f"{item}{comment}")
                    elif isinstance(comment, dict):
                        result.append(self._add_comments(item, comment))
                else:
                    result.append(item)
            return type(data)(result)
        return data

    def _dict_to_html(self, data, indent: int = 0) -> list[str]:
        html_lines = []
        indent_str = "&nbsp;" * indent
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list, tuple, set)):
                    html_lines.append(f"{indent_str}{key}:")
                    html_lines.extend(self._dict_to_html(value, indent + 2))
                else:
                    html_lines.append(f"{indent_str}{key}: {value}")
        elif isinstance(data, (list, tuple, set)):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list, tuple, set)):
                    if i != 0:
                        html_lines.append(f"{indent_str}")
                    html_lines.extend(self._dict_to_html(item, indent + 2))
                else:
                    html_lines.append(f"{indent_str}- {item}")
        else:
            html_lines.append(f"{indent_str}{data}")
        return html_lines
