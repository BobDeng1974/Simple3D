#include "test/GLTest.h"
#include "utils/GP_Clock.h"
#include <sstream>
#include <iostream>
#include "math/FormulaTree.h"
#include "math/BasicFunctionDeter.h"
#include <fstream>
using namespace std;
int main()
{
    std::ifstream is("function.txt");
    BasicFunctionDeter deter(is);
    FormulaTree _test(&deter);
    string x = string("cos(u)*cos(v)");
    string y = string("cos(u)*sin(v)");
    string z = string("sin(u)");
    _test.setFormula(z);
    _test.expand(cout);
    cout << endl;

    GPPtr<FormulaTree> detu = _test.detByName("u");
    detu->expand(std::cout);
    cout << endl;

    ostringstream tempOs;
    _test.expand(tempOs);

    _test.setFormula(tempOs.str());
    _test.expand(cout);
    cout << endl;

    //FormulaTree tree(&deter);
    //tree.setFormula("x*y+p-q*exp(u, v)");
    //tree.expand(std::cout);

    //string s("u");
    //GPPtr<FormulaTree> detTree = tree.detByName(s);
    //detTree->expand(std::cout);
    return 1;
}