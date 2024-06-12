#include "headers/campaign.hpp"
#include "headers/seeds.hpp"
#include "headers/coverage.hpp"
#include <random>

void Campaign::mutate(std::string& input) {
    // IMPLEMENT HERE
}

Seeds::Set Campaign::update_seeds(const Coverage::Set& coverage, const Coverage::Set& new_coverage, const std::string& mutant, const Seeds::Set& seeds) {
    Seeds::Set new_seeds = seeds;

    // IMPLEMENT HERE

    return new_seeds;
}

std::pair<Seeds::Set, Coverage::Set> Campaign::run(Environ& env, bool (*test)(Environ&, const std::string&), const std::pair<Seeds::Set, Coverage::Set>& seeds_and_coverage) {
    // SAMPLE USAGE
    Seeds::Set seeds = seeds_and_coverage.first;
    Coverage::Set coverage = seeds_and_coverage.second;
    Seeds::Set new_seeds;
    Coverage::Set new_coverage;

    // IMPLEMENT HERE; 

    // SAMPLE USAGE
    mutate(mutant);
    test(env, mutant); // You can call Fuzzer::test() in fuzzer.cpp by using function pointer
    new_coverage = Coverage::read(env.coverage_file);
    new_seeds = update_seeds(coverage, new_coverage, mutant, seeds);

    return std::make_pair(new_seeds, new_coverage);
}