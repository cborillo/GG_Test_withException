from ..utils.image_utils import append_images_to_messages


def get_evaluation_prompt(images, classification, extraction):
    """Generates a prompt for evaluating key/value pair extractions from health benefit claim images.

    Args:
    ----
        images (list): List of images to be processed.
        classification (str): Type of the health benefit claim form.
        extraction (dict): Extracted key/value pairs to be evaluated.

    Returns:
    -------
        list: Messages including the system role and content for evaluation.

    """
    messages = [
        {
            "role": "system",
            "content": f"""
            You are an AI assistant tasked with determining a confidence level for key/value pair extraction from complex {classification} Health Benefit Claim images for an insurance company. Your goal is to evaluate the quality of the extracted key/value pairs from the provided images. Please follow these guidelines:

            Criteria for Evaluation and Weighting:
                1. Clarity (25%): How clear and readable is the text in the image?
                2. Consistency (50%): How consistent is the extracted key/value pair with the text in the image?
                3. Relevance (25%): How relevant is the extracted key/value pair to the context of the image and form type?

            Confidence Levels: Calculate the weighted average of the three criteria scores to determine the overall confidence level for each key/value pair.

            Additional Information for Confidence Level Assignment:
                1. If a value is missing in both the extraction and the image, assign a confidence level of 1.0.
                2. A confidence level should be provided for all key/value pairs in the extraction and can be on a gradient between 0.0 and 1.0.
            
            Feedback Mechanism: Note any patterns or common issues observed during the evaluation to help improve future extraction processes.

            Average Confidence Level: After evaluating a confidence level for all key/value pairs, provide an average confidence level calculated as the sum of all confidence scores divided by the number of key/value pairs.

            Output your result in only JSON format. The format must be valid JSON with property names enclosed with quotes. If the extraction contains an array of values, then each object in the array should be evaluated separately.

            Example JSON output:

            {{
                "employee_info": {{
                    "employee_name": {{
                        "confidence": 0.925,
                    }},
                    "date_of_birth": {{
                        "confidence": 0.775,
                    }}
                }},
                "service_lines": [
                    {{
                        "procedure_code": {{
                            "confidence": 0.85,
                        }}
                    }}
                ],
                "average_confidence_level": 0.85,
                "feedback": "The image quality for dates could be improved. Consider enhancing OCR for numerical fields."
            }}

            Extracted Key/Value Pairs:

            {extraction}

            Images:
            """,
        },
    ]

    return append_images_to_messages(images, messages)
