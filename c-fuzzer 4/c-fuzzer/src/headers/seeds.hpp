#pragma once

#include <boost/container/set.hpp>
#include <string>

class Seeds {
public:
    using Set = boost::container::set<std::string>;

    static Set read(const std::string& dir);
};
