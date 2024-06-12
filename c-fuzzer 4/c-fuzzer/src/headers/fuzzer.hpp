#pragma once

#include <string>
#include "seeds.hpp"
#include "coverage.hpp"
#include "campaign.hpp"

class Fuzzer {
public:
    static void initialize(const Environ& env);
    static bool execute(const std::string& exe, const std::string& input);
    static void store_passing_input(Environ& env, const std::string& input);
    static void store_crashing_input(Environ& env, const std::string& input);
    static void gcov(const std::string& exe);
    static bool test(Environ& env, const std::string& input);
    static void run(Environ& env, const std::pair<Seeds::Set, Coverage::Set>& seeds_and_coverage);
};
