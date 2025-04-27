#include "db_sessions.h"
#include <stdexcept>
#include <fstream>
#include <string>
#include <sstream>

const std::string CREATE_TABLE_PATH{"create_tables.sql"};

Session::Session(const std::string path) {
    int code = sqlite3_open(path.c_str(), &DB);
    if (code != SQLITE_OK) {
        throw std::runtime_error("Failed to open sqlite3 database");
    }
    std::ifstream ifs{CREATE_TABLE_PATH};
    std::ostringstream oss;
    oss << ifs.rdbuf();
    std::string sql_create_tables = oss.str();
    code = sqlite3_exec(DB, sql_create_tables.c_str(), 0, 0, 0);
    if (code != SQLITE_OK) {
        throw std::runtime_error("Failed to create tables");
    }
}

Session::~Session() {
    sqlite3_close(DB);
}
