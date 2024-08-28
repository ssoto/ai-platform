import logging
import platform

from diffusers import DiffusionPipeline
from diffusers.models import AutoencoderKL
from diffusers import StableDiffusionPipeline
import torch

from ai_platform.domain.image_tasks.models import ImageTask

logger = logging.getLogger(__name__)

MACOS = 'macOS'
APPLE_SILICON_DEVICE = 'mps'


def startup_pipeline(only_download=False):
    logger.info(f"Starting pipeline")
    # https://huggingface.co/docs/diffusers/tutorials/basic_training
    # pipe = DiffusionPipeline.from_pretrained(
    #     "runwayml/stable-diffusion-v1-5",
    #     torch_dtype=torch.float16,
    #     variant="fp16",
    # )
    logger.info("Loading VAE model")
    vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")

    model = "CompVis/stable-diffusion-v1-4"
    logger.info(f"Loading model: {model}")
    pipe = StableDiffusionPipeline.from_pretrained(
        model,
        vae=vae
    )

    if only_download:
        return

    if torch.cuda.is_available():
        pipe.to("cuda")
    elif MACOS in platform.platform():
        pipe.to(APPLE_SILICON_DEVICE)

    # pipe.safety_checker = None
    # pipe.requires_safety_checker = False

    prompt = "fake prompt to wwarmup the pipeline"
    logger.info("Warming up the pipeline")
    # First-time "warmup" pass if PyTorch version is 1.13
    _ = pipe(prompt, num_inference_steps=1)
    logger.info("Pipeline warmed up")

    return pipe


def create_image(pipe: DiffusionPipeline, image: ImageTask):
    kwargs = {}
    if image.seed is not None:
        generator = torch.Generator(device="cpu").manual_seed(image.seed)
        kwargs["generator"] = generator

    kwargs["prompt"] = image.prompt
    kwargs["num_inference_steps"] = image.generation_steps

    # Results match those from the CPU device after the warmup pass.
    result = pipe(**kwargs)
    image_file = result.images[0]
    logger.info(f"Image generated: {image_file}")
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
    logger.info("Starting image generation pipeline")
    args = parse_args()
    startup_pipeline(only_download=True)
    if args.download_model:
        return


if __name__ == "__main__":
    main()
