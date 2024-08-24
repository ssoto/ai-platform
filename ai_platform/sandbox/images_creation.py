from diffusers import DiffusionPipeline
from pathlib import Path
import torch

from ai_platform.domain.images.models import ImageTask
from ai_platform.domain.images.use_cases import update_image_task

HERE = Path(__file__).resolve().parent
PROJECT_PATH = HERE.parent.parent
IMAGES_PATH = PROJECT_PATH / "images"
_pipe = None


def startup_pipeline():
    global _pipe
    _pipe = DiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16,
        variant="fp16",
    ).to("mps")
    _pipe.safety_checker = None
    _pipe.requires_safety_checker = False

    prompt = "a photo of a dog of white color"
    # First-time "warmup" pass if PyTorch version is 1.13
    _ = _pipe(prompt, num_inference_steps=1)


def generate_image(image: ImageTask):
    # Results match those from the CPU device after the warmup pass.
    global _pipe
    try:
        steps = 30
        result = _pipe(
            image.prompt,
            num_inference_steps=steps
        )
        file_path = IMAGES_PATH / f"{image.id}.png"
        image_file = result.images[0]
        image_file.save(file_path)
        image.set_completed()
    except Exception as e:
        image.set_failed(reason=repr(e))
    finally:
        update_image_task(image)


