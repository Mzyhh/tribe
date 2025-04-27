#include "db_sessions.h"
#include <stdexcept>
#include <sstream>

Session::Session(const std::string& path) {
    int code = sqlite3_open(path.c_str(), &DB);
    if (code != SQLITE_OK) {
        throw std::runtime_error("Failed to open sqlite3 database");
    }
}

void Session::execute(const std::ifstream& sql_file) {
    std::ostringstream oss;
    oss << sql_file.rdbuf();
    this->execute(oss.str());
    return;
}

void Session::execute(const std::string& sql_query) {
    int code = sqlite3_exec(DB, sql_query.c_str(), 0, 0, 0);
    if (code != SQLITE_OK) {
        throw std::runtime_error(std::string("Failed to execute query: ") + sql_query.substr(0, ERROR_MSG_LEN));
    }
    return;
}

Session::~Session() noexcept{
    sqlite3_close(DB);
}
