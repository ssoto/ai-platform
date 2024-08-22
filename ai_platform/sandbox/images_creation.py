from diffusers import DiffusionPipeline
from pathlib import Path
import torch

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


def generate_image(prompt, image_name):
    # Results match those from the CPU device after the warmup pass.
    global _pipe
    result = _pipe(prompt)
    image = result.images[0]
    file_path = IMAGES_PATH / f"{image_name}.png"
    image.save(file_path)
