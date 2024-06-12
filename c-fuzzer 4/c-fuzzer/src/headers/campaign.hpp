#pragma once

#include <string>
#include "seeds.hpp"
#include "coverage.hpp"

struct Environ {
    std::string exe;
    std::string seed_input_dir;
    std::string output_dir;
    std::string coverage_file;
    int pass;   // pass counter
    int crash;  // crash counter
};

class Campaign {
public:
    static void mutate(std::string& input);
    static std::pair<Seeds::Set, Coverage::Set> run(Environ& env, bool (*test)(Environ&, const std::string&), const std::pair<Seeds::Set, Coverage::Set>& seeds_and_coverage);
    static Seeds::Set update_seeds(const Coverage::Set& coverage, const Coverage::Set& new_coverage, const std::string& mutant, const Seeds::Set& seeds);
};
