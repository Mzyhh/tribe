#ifndef __DB_SESSIONS_H__
#define __DB_SESSIONS_H__
#include <sqlite3.h>
#include <string>


class Session {
public:
    Session(const std::string path=":memory:");

    ~Session();
private:
    sqlite3* DB;
};

#endif // __DB_SESSIONS_H__
