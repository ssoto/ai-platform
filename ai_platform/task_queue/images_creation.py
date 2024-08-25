import logging
import platform

from diffusers import DiffusionPipeline
import torch

from ai_platform.domain.image_tasks.models import ImageTask


def startup_pipeline(only_download=False):
    pipe = DiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16,
        variant="fp16",
    )
    if only_download:
        return

    if 'macOS' in platform.platform():
        pipe.to("mps")

    pipe.safety_checker = None
    pipe.requires_safety_checker = False

    prompt = "fake prompt to wwarmup the pipeline"
    logging.info("Warming up the pipeline")
    # First-time "warmup" pass if PyTorch version is 1.13
    _ = pipe(prompt, num_inference_steps=1)
    logging.info("Pipeline warmed up")

    return pipe


def create_image(pipe: DiffusionPipeline, image: ImageTask):
    # Results match those from the CPU device after the warmup pass.
    result = pipe(
        image.prompt,
        num_inference_steps=image.generation_steps
    )
    image_file = result.images[0]
    logging.info(f"Image generated: {image_file}")
    return image_file


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


if __name__ == "__main__":
    main()
