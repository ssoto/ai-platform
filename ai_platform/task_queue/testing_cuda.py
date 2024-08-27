import platform
from diffusers import StableDiffusionPipeline
import torch

MAC_OS = 'macOS'
APPLE_SILICON_DEVICE = 'mps'

model_id = "runwayml/stable-diffusion-v1-5"
output = "output.png"
prompt = "a cat looking through a glass fish bowl"

pipe = StableDiffusionPipeline.from_pretrained(model_id, variant="fp16", torch_dtype=torch.float16)

if torch.cuda.is_available():
    pipe = pipe.to("cuda")

if MAC_OS in platform.platform():
    pipe.to(APPLE_SILICON_DEVICE)

image = pipe(prompt).images[0]

image.save(output)
