## Run 'stable-diffusion-webui' in docker
docker run -it --name stable-diffusion-webui -v LOCATION:/app:ro bitnami/python:3.12 bash setup.sh

## Run 'ComfyUI' in docker
docker run -it --name comfyui -v LOCATION:/app:ro bitnami/python:3.12 bash setup.sh
# error: RuntimeError: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx

## Run 'fooocus' in docker
docker run -p 7865:7865 -v fooocus-data:/content/data -it ghcr.io/lllyasviel/fooocus bash setup.sh
# error: RuntimeError: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx
