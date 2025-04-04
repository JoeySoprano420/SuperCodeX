# Makefile for SuperCodeX Project

# Compiler and toolchain settings
CC = ./supercodex-compiler        # Path to the SuperCodeX compiler executable
ASM = nasm                        # Assembly compiler (x64 assembler)
LINKER = gcc                      # Linker for final binary
RUNNER = ./supercodex-runner      # Runtime execution environment
TARGET = supercodex_project.exe   # Output target file (Windows executable)

# Directories
SRC_DIR = src                     # Directory where .scdx source files are located
BUILD_DIR = build                 # Directory for compiled intermediary files
BIN_DIR = bin                     # Directory for the final executable
LIB_DIR = lib                     # Directory for any static libraries or external modules

# Compiler flags
COMPILE_FLAGS = --optimize --aot --mem-alloc --parallel
ASSEMBLY_FLAGS = -f win64 -g

# Source files
SRC_FILES = $(wildcard $(SRC_DIR)/*.scdx)  # All SuperCodeX source files in src/
OBJ_FILES = $(patsubst $(SRC_DIR)/%.scdx, $(BUILD_DIR)/%.obj, $(SRC_FILES))

# Assembly and object files (for intermediate steps)
ASM_FILES = $(patsubst $(SRC_DIR)/%.scdx, $(BUILD_DIR)/%.asm, $(SRC_FILES))
OBJ_ASM_FILES = $(patsubst $(SRC_DIR)/%.scdx, $(BUILD_DIR)/%.obj, $(SRC_FILES))

# Default target
all: $(BIN_DIR)/$(TARGET)

# Compile .scdx files into .asm using the SuperCodeX compiler
$(BUILD_DIR)/%.asm: $(SRC_DIR)/%.scdx
	$(CC) $(COMPILE_FLAGS) -o $@ $<

# Assemble .asm files into object files (.obj)
$(BUILD_DIR)/%.obj: $(BUILD_DIR)/%.asm
	$(ASM) $(ASSEMBLY_FLAGS) -o $@ $<

# Link object files and libraries to create the final executable
$(BIN_DIR)/$(TARGET): $(OBJ_FILES)
	$(LINKER) -o $@ $^ -L$(LIB_DIR) -lSuperCodeXRuntime -lm

# Clean up build directory
clean:
	rm -rf $(BUILD_DIR)/* $(BIN_DIR)/*

# Run the final executable
run: $(BIN_DIR)/$(TARGET)
	$(RUNNER) $(BIN_DIR)/$(TARGET)

# Generate a debug version (with debug info)
debug: $(BUILD_DIR)/debug/$(TARGET)
	$(CC) $(COMPILE_FLAGS) --debug -o $(BUILD_DIR)/debug/$(TARGET) $(SRC_FILES)

# This will print the build status and other info (optional)
status:
	@echo "SuperCodeX Build Status"
	@echo "Source Files: $(SRC_FILES)"
	@echo "Object Files: $(OBJ_FILES)"
	@echo "Assembly Files: $(ASM_FILES)"
	@echo "Final Executable: $(BIN_DIR)/$(TARGET)"
	@echo "Build Directory: $(BUILD_DIR)"
	@echo "Bin Directory: $(BIN_DIR)"
	@echo "Lib Directory: $(LIB_DIR)"
