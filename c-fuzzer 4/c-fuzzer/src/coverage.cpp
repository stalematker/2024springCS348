#include "headers/coverage.hpp"
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>

Coverage::Set Coverage::read(const std::string& coverage_file) {
    Set coverage;
    std::ifstream file(coverage_file);
    std::string line;

    if (file.is_open()) {
        while (std::getline(file, line)) {
            std::istringstream iss(line);
            std::string token;
            std::getline(iss, token, ':'); // Split by ':'
            token.erase(token.begin(), std::find_if(token.begin(), token.end(), boost::container::bind1st(std::not_equal_to<char>(), ' ')));
            int count = 0;
            // Check if the hit count is valid
            if (!token.empty() && token.find_first_not_of("-#=") == std::string::npos) count = 0;
            else count = 1;
            // Get the line number
            std::getline(iss, token);
            int line_number = std::stoi(token);
            // Add the line number to coverage if count is non-zero
            if (count > 0)
                coverage.insert(line_number);
        }
        file.close();
    }

    return coverage;
}