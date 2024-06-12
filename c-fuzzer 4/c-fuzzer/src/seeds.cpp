#include "headers/seeds.hpp"
#include <fstream>
#include <string>
#include <boost/bind.hpp>
#include <filesystem> 

Seeds::Set Seeds::read(const std::string& dir) {
    Set seed_inputs;
    std::ifstream file;
    std::string line;

    for (const auto& entry : std::filesystem::directory_iterator(dir)) {
        file.open(entry.path());
        if (file.is_open()) {
            while (std::getline(file, line)) {
                seed_inputs.insert(line);
            }
            file.close();
        }
    }

    return seed_inputs;
}
