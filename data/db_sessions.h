#ifndef __DB_SESSIONS_H__
#define __DB_SESSIONS_H__
#include <sqlite3.h>
#include <string>
#include <fstream>

constexpr int ERROR_MSG_LEN = 40;

class Session {
public:
    Session(const std::string& path=":memory:");
 
    void execute(const std::ifstream& sql_file);
    void execute(const std::string& sql_query);
    ~Session() noexcept;
private:
    sqlite3* DB;
};

#endif // __DB_SESSIONS_H__
