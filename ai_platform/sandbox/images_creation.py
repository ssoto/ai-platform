from diffusers import DiffusionPipeline
import torch

from ai_platform.domain.image_tasks.models import ImageTask
from ai_platform.domain.image_tasks.use_cases import update_image_task
from ai_platform.domain.image_repository.use_cases import update_image_task

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

    prompt = "fake prompt to wwarmup the pipeline"
    # First-time "warmup" pass if PyTorch version is 1.13
    _ = _pipe(prompt, num_inference_steps=1)


def generate_image(image: ImageTask):
    # Results match those from the CPU device after the warmup pass.
    global _pipe
    try:
        result = _pipe(
            image.prompt,
            num_inference_steps=image.generation_steps
        )
        image_file = result.images[0]
        image_file.save(image.image_path)
        image.set_completed()
    except Exception as e:
        image.set_failed(reason=repr(e))
    finally:
        update_image_task(image)
