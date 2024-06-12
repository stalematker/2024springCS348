#pragma once

#include <boost/container/set.hpp>
#include <string>

class Coverage {
public:
    using Set = boost::container::set<int>;

    static Set read(const std::string& coverage_file);
};
