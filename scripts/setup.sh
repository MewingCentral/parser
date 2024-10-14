#!/bin/bash

#sudo apt-get update
#sudo apt-get upgrade -y

# Add running shell.sh to the bashrc
echo "source $(pwd)/scripts/shell.sh" >> ~/.bashrc

# source $(pwd)/scripts/shell.sh

# Install python dependencies
if [ `which nvidia-smi` ]; then
    echo "CUDA is available"
    poetry install --all-extras --with dev,llm-cuda
else
    echo "CUDA is not available"
    poetry install --all-extras --with dev,llm
fi

exit 0