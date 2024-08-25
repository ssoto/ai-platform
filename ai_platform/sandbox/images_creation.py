import logging
import platform

from diffusers import DiffusionPipeline
import torch

from ai_platform.domain.image_tasks.models import ImageTask
from ai_platform.domain.image_tasks.use_cases import update_image_task
from ai_platform.domain.image_repository.use_cases import update_image_task

_pipe = None


def startup_pipeline(only_download=False):
    global _pipe
    _pipe = DiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16,
        variant="fp16",
    )
    if only_download:
        return

    if 'macOS' in platform.platform():
        _pipe.to("mps")

    _pipe.safety_checker = None
    _pipe.requires_safety_checker = False

    prompt = "fake prompt to wwarmup the pipeline"
    logging.info("Warming up the pipeline")
    # First-time "warmup" pass if PyTorch version is 1.13
    _ = _pipe(prompt, num_inference_steps=1)
    logging.info("Pipeline warmed up")


def generate_image(image: ImageTask):
    # Results match those from the CPU device after the warmup pass.
    global _pipe
    try:
        result = _pipe(
            image.prompt,
            num_inference_steps=image.generation_steps
        )
        image_file = result.images[0]
        logging.info(f"Image generated: {image_file.shape}")
        image_file.save(image.image_path)
        image.set_completed()
    except Exception as e:
        image.set_failed(reason=repr(e))
    finally:
        update_image_task(image)
        logging.info(f"Process finished for image {image.id}")


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Image generation")
    parser.add_argument(
        "--download_model",
        default=False,
        help="Download the model",
        action="store_true",
    )

    return parser.parse_args()


def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    args = parse_args()
    startup_pipeline(only_download=True)
    if args.download_model:
        return

    # Testing the image generation
    image_task = ImageTask(
        prompt="A cat in the snow",
        generation_steps=10,
    )
    image_task.set_processing()
    generate_image(image_task)


if __name__ == "__main__":
    main()
