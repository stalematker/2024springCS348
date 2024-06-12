#include "headers/fuzzer.hpp"
#include "headers/campaign.hpp"
#include <iostream>
#include <fstream>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/wait.h>

void Fuzzer::initialize(const Environ& env) {
    mkdir((env.output_dir + "/pass").c_str(), 0755);
    mkdir((env.output_dir + "/crash").c_str(), 0755);
}

bool Fuzzer::execute(const std::string& exe, const std::string& input) {
    int fd_in[2];
    pipe(fd_in);
    int fd_out = open("/dev/null", O_WRONLY);
    pid_t pid = fork();

    if (pid == 0) {
        close(fd_out);
        close(fd_in[1]);
        close(0);
        dup(fd_in[0]);
        close(fd_in[0]);
        execl(exe.c_str(), exe.c_str(), nullptr);
        exit(0);
    } else {
        close(fd_out);
        write(fd_in[1], (input + "\n").c_str(), input.size() + 1);
        close(fd_in[1]);
        int status;
        waitpid(pid, &status, 0);
        return WIFEXITED(status) && WEXITSTATUS(status) == 0;
    }
}

void Fuzzer::store_passing_input(Environ& env, const std::string& input) {
    std::ofstream file(env.output_dir + "/pass/input" + std::to_string(env.pass));
    file << input << "\n";
    file.close();
    env.pass++;
}

void Fuzzer::store_crashing_input(Environ& env, const std::string& input) {
    std::ofstream file(env.output_dir + "/crash/input" + std::to_string(env.crash));
    file << input << "\n";
    file.close();
    env.crash++;
}

void Fuzzer::gcov(const std::string& exe) {
    // Assuming gcov is in the system PATH
    system(("gcov " + exe).c_str());
}

bool Fuzzer::test(Environ& env, const std::string& input) {
    try {
        if (execute(env.exe, input)) {
            store_passing_input(env, input);
            gcov(env.exe);
            return true;
        } else {
            store_crashing_input(env, input);
            std::cout << env.crash << " crashes occurs\n";
            gcov(env.exe);
            return false;
        }
    } catch (...) {
        std::cerr << "WARNING: error occurred while executing the fuzzer.\n";
        return false;
    }
}

void Fuzzer::run(Environ& env, const std::pair<Seeds::Set, Coverage::Set>& seeds_and_coverage) {
    Environ temp_env = env;
    auto seeds = seeds_and_coverage.first;
    auto coverage = seeds_and_coverage.second;
    while (true) {
        auto result = Campaign::run(temp_env, test, {seeds, coverage});
        seeds = result.first;
        coverage = result.second;
    }
}