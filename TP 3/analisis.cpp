#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <vector>
using namespace std;

int main() {
    vector <vector <string> > data;
    string ifile = "checkins_places.txt", ofile = "loc-brightkite_totalCheckins.txt";
    ifstream myin(ifile.c_str());
    ofstream myout(ofile.c_str());
    string num;
    vector <string> f;
    while (myin >> num) {
        f.push_back(num);
        if (f.size() == 4) {
            data.push_back(f);
            f.clear();
        }
    }
    int n = data.size();
    int i = 0;
    for(i=0;i<n;i++){
        myout << data[i][0] << '\t' << data[i][1] << endl;
    }
}