import math
import logging
from io import BytesIO

import allure
from PIL import Image
from pixelmatch.contrib.PIL import pixelmatch


@allure.step("Compaing original and uploaded pictures")
def step_compare_uploaded_images(
    original_image: str, uploaded_image: str,
    uploaded_image_content: bytes,
    threshold: float = 0.2, fail_fast: bool = True
):
    """Compares original image and image uploaded to server.

    Uploaded image is expected to be scaled to 480x480,
    saving aspect ratio and with canvas resize. Extra space
    is expectd to be filled with plain white.

    Function will apply similar chnages to original image
    and then compare both.

    Args:
        original_image (str): path to image.
        uploaded_image (str): url to image.
        uploaded_image_content (bytes): downloaded image as bytes.
        threshold (optional, float): comparison threshold (0...1,
        bigger more tolerant). Defaults to 0.2.
        fail_fast (optional, bool): fail on any level of errors.
        Defaults to True.
    """

    logging.info(
        'Image comparison started for image: original = %s, target = %s',
        original_image, uploaded_image
    )

    src_img = Image.open(original_image)
    tgt_img = Image.open(BytesIO(uploaded_image_content))

    # --- Resize source image, saving aspect ratio
    w, h = src_img.size
    aspect = w / h
    tgt_w, tgt_h = tgt_img.size

    if aspect > 1:
        new_w = tgt_w
        new_h = int(round(tgt_h/aspect))
    elif aspect < 1:
        new_w = int(round(tgt_w * aspect))
        new_h = tgt_h
    else:
        new_w, new_h = tgt_w, tgt_h

    src_img = src_img.resize((new_w, new_h))

    w, h = src_img.size

    # Center the image
    x1 = int(math.floor((tgt_w - w) / 2))
    y1 = int(math.floor((tgt_h - h) / 2))

    mode = src_img.mode
    if len(mode) == 1:  # L, 1
        new_background = 255
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    new_image = Image.new(mode, (tgt_w, tgt_h), new_background)
    new_image.paste(src_img, (x1, y1, x1 + w, y1 + h))
    img_diff = Image.new("RGBA", tgt_img.size)

    src_img_bytes = BytesIO()
    new_image.save(src_img_bytes, format='PNG')

    tgt_img_bytes = BytesIO()
    tgt_img.save(tgt_img_bytes, format='PNG')

    allure.attach(
        body=src_img_bytes.getvalue(),
        name="Original image (resized)",
        extension=allure.attachment_type.PNG
    )
    allure.attach(
        body=tgt_img_bytes.getvalue(),
        name="Uploaded image",
        extension=allure.attachment_type.PNG
    )

    mismatch = pixelmatch(
        new_image, tgt_img, img_diff,
        threshold=threshold,
        fail_fast=fail_fast
    )
    print(f'Image comparison error is {mismatch}')
    logging.info('Image comparison error is %s', mismatch)

    assert mismatch == 0, f"Images differs (error: {mismatch})"
