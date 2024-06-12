#include "headers/fuzzer.hpp"
#include "headers/seeds.hpp"
#include "headers/coverage.hpp"
#include "headers/campaign.hpp"
#include <iostream>
#include <string>
#include <filesystem>

void sanity_check(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "usage: fuzzer [executable] [seed input dir] [output dir]" << std::endl;
        exit(1);
    }
    if (!std::filesystem::exists(argv[1])) {
        std::cerr << argv[1] << " not found" << std::endl;
        exit(1);
    }
    if (!std::filesystem::exists(argv[2])) {
        std::cerr << argv[2] << " not found" << std::endl;
        exit(1);
    }
    if (!std::filesystem::exists(argv[3])) {
        std::filesystem::create_directory(argv[3]);
    }
}

int main(int argc, char* argv[]) {
    sanity_check(argc, argv);

    Environ env = {
        .exe = argv[1],
        .seed_input_dir = argv[2],
        .output_dir = argv[3],
        .coverage_file = std::string(argv[1]) + ".c.gcov",
        .pass = 0,
        .crash = 0
    };

    Fuzzer::initialize(env);
    auto seeds = Seeds::read(env.seed_input_dir);
    auto coverage = Coverage::Set(); // Assuming empty coverage set for now
    Fuzzer::run(env, {seeds, coverage});

    return 0;
}
