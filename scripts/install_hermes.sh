#!/bin/bash

# Define the URLs for each quantization level
declare -A urls
urls[4]="https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF/resolve/main/Hermes-2-Pro-Llama-3-8B-Q4_K_M.gguf"
urls[5]="https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF/resolve/main/Hermes-2-Pro-Llama-3-8B-Q5_K_M.gguf"
urls[6]="https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF/resolve/main/Hermes-2-Pro-Llama-3-8B-Q6_K.gguf"
urls[8]="https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF/resolve/main/Hermes-2-Pro-Llama-3-8B-Q8_0.gguf"
urls[16]="https://huggingface.co/NousResearch/Hermes-2-Pro-Llama-3-8B-GGUF/resolve/main/Hermes-2-Pro-Llama-3-8B-F16.gguf"

# Prompt the user for the desired quantization level
echo "Please enter the quantization level you want to download (4, 5, 6, 8, 16):"
read quantization_level

# Check if the entered quantization level is valid
if [[ -z "${urls[$quantization_level]}" ]]; then
    echo "Invalid quantization level. Please enter one of the following: 4, 5, 6, 8, 16."
    exit 1
fi

# Create the models directory if it does not exist
mkdir -p ../models

# Download the model to the models directory
wget -O ../models/Hermes-2-Pro-Llama-3-8B-Q${quantization_level}.gguf "${urls[$quantization_level]}"

echo "Download complete. The model has been saved to ../models/Hermes-2-Pro-Llama-3-8B-Q${quantization_level}.gguf"
