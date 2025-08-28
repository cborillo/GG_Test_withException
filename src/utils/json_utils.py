from __future__ import annotations

import json


def extract_json(response):
        json_start = response.index("{")
        json_end = response.rfind("}")
        extraction = response[json_start : json_end + 1]
        return json.loads(extraction)



def merge_extraction_and_evaluation(extraction, evaluation):
    """
    Merge extraction and evaluation dictionaries to a single dictionary.
    """

    def merge_nested_dicts(extract_dict, eval_dict):
        merged_dict = {}

        if not eval_dict:  #In the case that evaluation exceeds max token size and return empty value
            for key, extract_value in extract_dict.items():
                if isinstance(extract_value, dict):
                    # Recursively merge nested dictionaries
                    merged_dict[key] = merge_nested_dicts(extract_value, {})
                elif isinstance(extract_value, list):
                    if not extract_value:
                        merged_dict[key] = extract_value
                    else:
                        # Recursively merge nested lists
                        merged_list = [(merge_nested_dicts(item, {}))for item in extract_value]
                        merged_dict[key] = merged_list
                else:
                    merged_dict[key] = {
                    "value": extract_value,
                    "confidence": 0.5,
                }
                    
            return merged_dict

        for key, extract_value in extract_dict.items():
            eval_value = eval_dict.get(key)

            if isinstance(extract_value, dict):
                # Recursively merge nested dictionaries
                merged_dict[key] = merge_nested_dicts(extract_value, eval_value or {})
            elif isinstance(extract_value, list) and isinstance(eval_value, list):
                # Recursively merge nested lists
                merged_list = [
                    (
                        merge_nested_dicts(item, eval_item)
                        if isinstance(item, dict) and isinstance(eval_item, dict)
                        else item
                    )
                    for item, eval_item in zip(extract_value, eval_value)
                ]
                # Append remaining items from eval_value if it has more elements
                merged_list.extend(eval_value[len(extract_value) :])
                merged_dict[key] = merged_list
            elif isinstance(eval_value, dict) and "confidence" in eval_value:
                if isinstance(extract_value, list) and not extract_value:
                    merged_dict[key] = extract_value
                else:
                    merged_dict[key] = {
                        "value": extract_value,
                        "confidence": eval_value.get("confidence", 0.5),
                    }
            else:
                merged_dict[key] = {
                    "value": extract_value,
                    "confidence": 0.5,
                }

        return merged_dict

    return merge_nested_dicts(extraction, evaluation)


def reverse_merge(data: dict | list) -> dict | list:
    """This function effectively reverse json_utils.merge_extraction_and_evaluation
    to be able to parse it back to the original pydantic model.
    """
    if isinstance(data, dict):
        if "value" in data:
            return data["value"]
        return {key: reverse_merge(value) for key, value in data.items()}
    if isinstance(data, list):
        return [reverse_merge(item) for item in data]
    return data
