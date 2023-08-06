import argparse, json, os
from loguru import logger
from beartype import beartype
from sahi.model import Yolov5DetectionModel
from sahi.predict import get_sliced_prediction


@beartype
def mkdir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


@beartype
def get_files(input_directory: str):
    logger.info("Input Directory: {}".format(input_directory))
    for root, dirs, files in os.walk(input_directory, topdown=False):
        for name in files:
            if name.endswith((".jpg", ".jpeg", ".gif", ".png")):
                # Get the full file path
                full_file_path = os.path.join(root, name)

                # Get the relative file path
                relative_file_path = os.path.relpath(
                    full_file_path,
                    input_directory,
                )

                yield {
                    "name": name,
                    "full_file_path": full_file_path,
                    "relative_file_path": relative_file_path,
                }


@beartype
def write_json_line(writer, line) -> None:
    writer.write(json.dumps(line))
    writer.write("\n")


@beartype
def writer_close(writer) -> None:
    writer.close()


def main(args):

    # Create the directory structure
    mkdir(os.path.dirname(args["output_manifest_file"]))

    logger.debug("Loading the model {}".format(args["model_path"]))

    detection_model = Yolov5DetectionModel(
        model_path=args["model_path"],
        confidence_threshold=args["confidence_threshold"],
        device=args["device"],
    )

    # Get all of the files in the input data path
    files = get_files(args["input_directory"])

    # Open the jsonl output file writer
    with open(args["output_manifest_file"], "w") as writer:

        for idx, file in enumerate(files, start=1):

            logger.debug("Processing image {}".format(file["full_file_path"]))

            # Get the object preductions
            object_predictions = get_sliced_prediction(
                file["full_file_path"],
                detection_model,
                slice_width=args["slice_width"],
                slice_height=args["slice_height"],
                overlap_height_ratio=args["overlap_height_ratio"],
                overlap_width_ratio=args["overlap_width_ratio"],
                perform_standard_pred=False,
            )

            coco_predictions = object_predictions.to_coco_predictions()

            logger.debug(
                "Saving detections for image {}".format(file["full_file_path"])
            )

            for idx, coco_prediction in enumerate(coco_predictions):
                coco_predictions[idx]["image_name"] = file["name"]
                write_json_line(writer, coco_prediction)

            # TODO: Save the predictions to disk
            # object_predictions.export_visuals(export_dir="./models/{}/".format(type))
            # os.rename(
            #     "./models/{}/prediction_visual.png".format(type),
            #     "./models/{}/{}.png".format(type, os.path.basename(file_path)),
            # )

    # Close the writer
    writer_close(writer)


def app():
    parser = argparse.ArgumentParser(
        description="Provides a way to perform sliced inferencing on a directory of images."
    )

    parser.add_argument(
        "--input_directory",
        type=str,
        dest="input_directory",
        help="Path to the input directory (image data).",
        required=True,
    )

    parser.add_argument(
        "--output_manifest_file",
        type=str,
        dest="output_manifest_file",
        default="./tmp/manifest.coco-results.jsonl",
        help="Path to the output manifest file.",
        required=True,
    )

    parser.add_argument(
        "--model_path",
        type=str,
        dest="model_path",
        help="Path to model.",
        required=True,
    )

    parser.add_argument(
        "--confidence_threshold",
        type=float,
        dest="confidence_threshold",
        default=0.2,
        help="The confidence threshold of prediction scores.",
        required=True,
    )

    parser.add_argument(
        "--device",
        type=str,
        dest="device",
        default="cpu",
        help="The name of the device to run the model (e.g. cpu or cuda:0)",
        required=True,
    )

    parser.add_argument(
        "--slice_width",
        type=int,
        dest="slice_width",
        help="The slice width to inference.",
        required=True,
    )

    parser.add_argument(
        "--slice_height",
        type=int,
        dest="slice_height",
        help="The slice height to inference.",
        required=True,
    )

    parser.add_argument(
        "--overlap_width_ratio",
        type=float,
        dest="overlap_width_ratio",
        default=0,
        help="The overlap width ratio to inference.",
        required=True,
    )

    parser.add_argument(
        "--overlap_height_ratio",
        type=float,
        dest="overlap_height_ratio",
        default=0,
        help="The overlap height ratio to inference.",
        required=True,
    )

    args = vars(parser.parse_args())

    main(args)
