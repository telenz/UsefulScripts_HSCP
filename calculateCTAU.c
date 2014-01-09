#include<iostream>

void calculateCTAU(double Width){


  double hbar = 6.58212*pow(10,-24);  //[hbar]=GeV*s
  double c = 2.9979*pow(10,8);        //[c]=s

  double cTau = c*hbar/Width;         //[cTau]=m

  cout<<"cTau is "<<cTau<<" m."<<endl<<endl<<endl;

}
