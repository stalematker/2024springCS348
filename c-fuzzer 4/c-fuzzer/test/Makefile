CC=@gcc
RM=@rm

EXAMPLE_C_FILES = $(shell find . -type f -name '*.c' | grep -v "runtime.c")
EXAMPLE_BIN_FILES = $(patsubst %.c, %, $(filter %.c, $(EXAMPLE_C_FILES)))

all: $(EXAMPLE_BIN_FILES)

%: %.c
	$(CC) -ldl -lm -Wno-implicit-function-declaration -Wno-div-by-zero -fsanitize=integer-divide-by-zero --coverage -O0 -o $* $< -g

clean:
	$(RM) -f *.output *.c.gcov *.gcno *.gcda $(EXAMPLE_BIN_FILES)
