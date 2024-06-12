CC = g++
CFLAGS = -std=c++17 -Wall -Wextra -pedantic
SRC_DIR = ./src
HEADER_DIR = ./src/headers
BUILD_DIR = ./src
EXECUTABLE = fuzzer

# List of all source files
SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
# List of all header files
HEADERS = $(wildcard $(HEADER_DIR)/*.hpp)
# List of all object files
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SOURCES))

# Build the executable
$(EXECUTABLE): $(OBJECTS)
	$(CC) $(CFLAGS) $^ -o $@

# Build object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)/*.o $(EXECUTABLE)
