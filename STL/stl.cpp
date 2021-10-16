#include<iostream>
#include<array>
#include<vector>

using namespace std;

int main(){
    vector<int> v;
    v.push_back(1);
    v.push_back(3);
    v.push_back(1);
    v.push_back(7);
    v.push_back(1);
    cout<<"Capacity-->"<<v.capacity()<<"   Size-->"<<v.size();

    for (int i:v){
        cout<<i<<endl;
    }

}