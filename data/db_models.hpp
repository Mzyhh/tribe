#ifndef __DB_MODELS_H__
#define __DB_MODELS_H__
#include <string>
#include <chrono>

class Human {
    uint id;
    std::string name;
    std::string description;
    std::chrono::year_month_day birthday;
    std::chrono::year_month_day deathday;
};

class Family {
    uint id;
    std::string name;
};

class FamilyTie {
    const Human& lhuman;
    const Human& rhuman;
};

class FamilyTieType {
    uint id;
    std::string title;
};
#endif // __DB_MODELS_H__

