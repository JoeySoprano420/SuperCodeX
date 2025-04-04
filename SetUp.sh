#!/bin/bash

# Setup script for SuperCodeX Development Environment
# This script automates the setup of the SuperCodeX compiler, runtime, and build environment

# Check if the script is being run as root (for package installs)
if [ "$(id -u)" -eq 0 ]; then
  echo "Do not run this script as root!" 1>&2
  exit 1
fi

# Function to install dependencies (using apt for Ubuntu/Debian as example)
install_dependencies() {
    echo "Installing dependencies..."
    sudo apt update
    sudo apt install -y build-essential nasm gcc make git curl

    # Installing SuperCodeX Compiler
    echo "Installing SuperCodeX Compiler..."
    if [ ! -d "$HOME/supercodex" ]; then
        git clone https://github.com/yourrepo/supercodex.git $HOME/supercodex
    fi

    # Build SuperCodeX Compiler
    cd $HOME/supercodex
    make all

    # Installing runtime libraries
    echo "Installing runtime dependencies..."
    sudo make install-runtime
}

# Function to set up directories for project
setup_directories() {
    echo "Setting up project directories..."
    mkdir -p ~/SuperCodeX-Project/src
    mkdir -p ~/SuperCodeX-Project/build
    mkdir -p ~/SuperCodeX-Project/bin
    mkdir -p ~/SuperCodeX-Project/lib
}

# Function to download SuperCodeX libraries and set them up
setup_libraries() {
    echo "Downloading necessary libraries..."
    cd ~/SuperCodeX-Project/lib
    git clone https://github.com/yourrepo/supercodex-libs.git
    echo "Libraries set up successfully."
}

# Create the project structure
create_project() {
    echo "Creating new SuperCodeX project structure..."
    setup_directories
    setup_libraries

    echo "Project setup complete!"
}

# Function to initialize the Makefile
init_makefile() {
    echo "Initializing Makefile..."
    cat > ~/SuperCodeX-Project/Makefile << 'EOF'
# Makefile for SuperCodeX Project

CC = ./supercodex-compiler
ASM = nasm
LINKER = gcc
RUNNER = ./supercodex-runner
TARGET = supercodex_project.exe

SRC_DIR = src
BUILD_DIR = build
BIN_DIR = bin
LIB_DIR = lib

COMPILE_FLAGS = --optimize --aot --mem-alloc --parallel
ASSEMBLY_FLAGS = -f win64 -g

SRC_FILES = $(wildcard $(SRC_DIR)/*.scdx)
OBJ_FILES = $(patsubst $(SRC_DIR)/%.scdx, $(BUILD_DIR)/%.obj, $(SRC_FILES))

ASM_FILES = $(patsubst $(SRC_DIR)/%.scdx, $(BUILD_DIR)/%.asm, $(SRC_FILES))
OBJ_ASM_FILES = $(patsubst $(SRC_DIR)/%.scdx, $(BUILD_DIR)/%.obj, $(SRC_FILES))

all: $(BIN_DIR)/$(TARGET)

$(BUILD_DIR)/%.asm: $(SRC_DIR)/%.scdx
	$(CC) $(COMPILE_FLAGS) -o $@ $<

$(BUILD_DIR)/%.obj: $(BUILD_DIR)/%.asm
	$(ASM) $(ASSEMBLY_FLAGS) -o $@ $<

$(BIN_DIR)/$(TARGET): $(OBJ_FILES)
	$(LINKER) -o $@ $^ -L$(LIB_DIR) -lSuperCodeXRuntime -lm

clean:
	rm -rf $(BUILD_DIR)/* $(BIN_DIR)/*

run: $(BIN_DIR)/$(TARGET)
	$(RUNNER) $(BIN_DIR)/$(TARGET)

debug: $(BUILD_DIR)/debug/$(TARGET)
	$(CC) $(COMPILE_FLAGS) --debug -o $(BUILD_DIR)/debug/$(TARGET) $(SRC_FILES)

status:
	@echo "SuperCodeX Build Status"
	@echo "Source Files: $(SRC_FILES)"
	@echo "Object Files: $(OBJ_FILES)"
	@echo "Assembly Files: $(ASM_FILES)"
	@echo "Final Executable: $(BIN_DIR)/$(TARGET)"
	@echo "Build Directory: $(BUILD_DIR)"
	@echo "Bin Directory: $(BIN_DIR)"
	@echo "Lib Directory: $(LIB_DIR)"
EOF
    echo "Makefile initialized."
}

# Function to install additional configurations (optional)
install_configurations() {
    echo "Setting up global configurations..."
    # Custom configuration setup can be added here
}

# Main setup routine
echo "Starting SuperCodeX setup..."
install_dependencies
create_project
init_makefile
install_configurations

echo "SuperCodeX setup completed successfully."
