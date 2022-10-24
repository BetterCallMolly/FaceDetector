# https://github.com/Nuttyb0il/FaceDetector

import os
import traceback
import argparse
import logging
import requests
import cv2
from tqdm import tqdm
from glob import glob
from detecto.core import Model
from detecto import utils

MODEL_URL = "https://github.com/Nuttyb0il/FaceDetector/releases/download/v.1.0.0/fd_v100.pth"
MODEL_PATH = "./fd_v100.pth"
IMAGES_EXT = [".jpg", ".jpeg", ".png"]

is_image_file = lambda x: os.path.splitext(x)[1].lower() in IMAGES_EXT

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args(print_args: bool = True) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crop faces from all images in a folder"
    )
    parser.add_argument("--input", type=str, help="Input folder", required=True)
    parser.add_argument(
        "--threshold",
        type=float,
        help="Threshold for face detection (default: 0.85)",
        default=0.85,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output folder (default faces_output)",
        default="faces_output",
    )
    parser.add_argument(
        "--size",
        type=int,
        help="Size of cropped faces (works only if --resize is specified)",
        default=256,
    )
    parser.add_argument(
        "--resize",
        action="store_true",
        help="Resize faces to size argument if set (default 256x256)",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search for images recursively in input folder (default True)",
        default=True,
    )
    parser.add_argument(
        "--minimum_size",
        type=int,
        help="Minimum size of faces to be detected (default 96x96)",
        default=96,
    )
    parser.add_argument(
        "--extend_box",
        type=float,
        help="Extend the box around the face to capture more of the face (default x1.25)",
        default=1.25,
    )
    args = parser.parse_args()
    if print_args:
        print(args)
    return args


def download_model() -> bool:
    """
    Downloads the model from the GitHub release page
    :return: True if download was successful, False otherwise
    """
    logger.info("Model not found, downloading...")
    try:
        r = requests.get(MODEL_URL, allow_redirects=True, stream=True)
        total_size = int(r.headers.get("content-length", 0))
        block_size = 8192
        with open(MODEL_PATH, "wb+") as f:
            for data in tqdm(
                r.iter_content(block_size),
                total=total_size // block_size,
                unit="KB",
            ):
                f.write(data)
        return True
    except:
        traceback.print_exc()
        logger.error("Failed to download model, exiting...")
        return False


def crop_face(
    image_path: str,
    output_dir: str,
    extend_box: int,
    threshold: float,
    resize: bool,
    size: int,
) -> None:
    # Get a formatable output_path
    name_template = (
        os.path.basename(image_path).split(".")[0]
        + "_{}."
        + image_path.split(".")[-1]
    )
    try:
        image = utils.read_image(image_path)
        labels, boxes, scores = model.predict(image)
        keep_boxes = []
        if len(labels) >= 1:
            for box, score in zip(boxes, scores):
                if score > threshold:
                    keep_boxes.append(box)
        for i, box in enumerate(keep_boxes):
            # Extend top right and bottom left corners of the box
            x1, y1, x2, y2 = box
            x1 = int(x1 - (x2 - x1) * extend_box)
            y1 = int(y1 - (y2 - y1) * extend_box)
            x2 = int(x2 + (x2 - x1) * extend_box)
            y2 = int(y2 + (y2 - y1) * extend_box)
            # Crop the face
            face = image[box[1]:box[3], box[0]:box[2]]
            if resize:
                face = cv2.resize(face, (size, size))
            cv2.imwrite(os.path.join(output_dir, name_template.format(i)), face)
    except KeyboardInterrupt:
        logger.fatal("Caught a CTRL+C, exiting...")
        exit(1)
    except:
        pass


if __name__ == "__main__":
    args = parse_args()
    if not os.path.exists(MODEL_PATH) and not download_model():
        exit(1)
    logger.info("Loading model...")
    model = Model.load(MODEL_PATH, ["face"])
    logger.info("Model loaded")
    logger.info("Searching for images...")
    images = glob(args.input + "/**/*", recursive=args.recursive)
    images = list(filter(is_image_file, images))
    logger.info(f"Found {len(images)} images")
    os.makedirs(args.output, exist_ok=True)
    for image in tqdm(images, desc="Cropping faces", unit="images"):
        crop_face(
            image,
            args.output,
            args.extend_box,
            args.threshold,
            args.resize,
            args.size,
        )
