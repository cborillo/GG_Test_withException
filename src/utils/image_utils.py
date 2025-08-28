import base64
from io import BytesIO
import logging

import cv2
import numpy as np
from werkzeug.datastructures import FileStorage
from PIL import Image, ImageEnhance, ImageFile


def preprocess_for_ocr(
    image: Image.Image,
    enhance_contrast: float = 1.5,  # 1.0 means no change
    sharpen: float = 1.5,  # 1.0 means no change
) -> Image.Image:
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # bump contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(enhance_contrast)

    # bump sharpeness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(sharpen)

    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # to grayscale
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        src=gray,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=11,
        C=2,
    )

    # mild denoising
    denoised = cv2.fastNlMeansDenoising(
        src=thresh,
        dst=None,
        h=10,
        templateWindowSize=7,
        searchWindowSize=21,
    )

    return Image.fromarray(cv2.cvtColor(denoised, cv2.COLOR_GRAY2RGB))


def optimize_image(image: Image.Image, max_size=(1600, 1600), dpi=300) -> Image.Image:
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size, Image.LANCZOS)
    image.info["dpi"] = (dpi, dpi)
    return image


def crop_image(image: Image.Image, proportion: float = 0.5) -> Image.Image:
    width, height = image.size
    left = 0
    right = width
    top = 0
    bottom = int(height * proportion)
    return image.crop((left, top, right, bottom))


def convert_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")  # Use PNG for lossless compression
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def process_image(file: FileStorage, crop_proportion: float = 1) -> str:
    with Image.open(file.stream) as img:
        img = crop_image(img, crop_proportion)
        img = resize_image(img)
        base64_string = convert_to_base64(img)
    file.seek(0)  # reset file pointer
    return base64_string


def rotate_image(base64_string: str, rotation_angle: int | None) -> str:
    if rotation_angle is None:
        return base64_string
    try:
        # Decode the base64 string
        image_data = base64.b64decode(base64_string)
        # Create a BytesIO object from the decoded bytes
        image_file = BytesIO(image_data)

        # Open the image using PIL
        with Image.open(image_file) as img:
            # Normalize and adjust the rotation angle
            rotation_angle = rotation_angle % 360
            # Rotate the image
            rotated_img = img.rotate(
                rotation_angle, expand=True, resample=Image.BICUBIC
            )

            # Save the rotated image to a BytesIO object
            buffered = BytesIO()
            rotated_img.save(buffered, format=img.format or "PNG")
            buffered.seek(0)

            # Encode the BytesIO object to a base64 string
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return encoded_image

    except Exception as e:
        print(f"An error occurred: {e}")
        return base64_string


def resize_image(img: ImageFile, max_size=(4000, 4000)) -> ImageFile:
    """
    Resize the image to the specified max_size
    """
    try:
        if img.size[0] <= max_size[0] and img.size[1] <= max_size[1]:
            return img

        logging.info(f"Resizing image from {img.size} to {max_size}")

        # Resize the image
        resized_img = img.resize(
            (
                min(img.size[0], max_size[0]),
                min(img.size[1], max_size[1]),
            ),
            resample=Image.BICUBIC,
        )

        # Save the resized image to a BytesIO object
        buffered = BytesIO()
        resized_img.save(buffered, format=img.format or "PNG")

        logging.info("Image resized successfully")

        return resized_img

    except Exception as e:
        logging.info(f"An error occurred: {e}")
        return img


def append_images_to_messages(images, messages):
    for image in images:
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image}"},
                    },
                ],
            },
        )
    return messages
