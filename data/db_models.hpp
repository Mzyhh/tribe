#ifndef __DB_MODELS_H__
#define __DB_MODELS_H__
#include <string>
#include <chrono>


/// @table_name=families
class Family { 
    /// @pk @autoincrement
    uint id;
    /// @not_null
    std::string name;
};

/// @table_name=people
class Human
{
    /// @pk @autoincrement
    uint id; 
    /// @not_null
    std::string name;
    /// @fk=families
    const Family& family;
    std::string description;
    std::chrono::year_month_day birthday;
    std::chrono::year_month_day deathday;
};

/// @table_name=family_tie_types
class FamilyTieType {
    /// @pk @autoincrement
    uint id;
    /// @not_null @unique
    std::string title;
};

/// @table_name=family_ties
class FamilyTie {
    /// @fk=people
    const Human& lhuman;
    /// @fk=people
    const Human& rhuman;
    /// @fk=family_tie_types
    const FamilyTieType& type;
};

#endif // __DB_MODELS_H__

