#ifndef __DB_MODELS_H__
#define __DB_MODELS_H__
#include <sqlite3.h>

class Model {
};

class Human : public Model {
};

class Family : public Model {};

class FamilyTie : public Model {};

class FamilyTieType : public Model {};
#endif // __DB_MODELS_H__

