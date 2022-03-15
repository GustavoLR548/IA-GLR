#include <iostream>
#include <cstdlib>
#include <cmath>
#include <string>

int maxNumber(int a, int b)
{
    if (a>b)
        return a; 
    else 
        return b;
}

std::string addZeros(std::string s, int max) 
{
    max -= s.length();
    
    if ( max <= 0 )
        return s;
    
    std::string resp = "";
    while (max != 0) {
        resp += "0";
        max--;
    }
    
    for (int i = 0; i < s.length(); i++) {
        resp+= s.at(i);
    }
    
    return resp;
}

std::string toBinary(int n)
{
    std::string r;
    while(n!=0) {r=(n%2==0 ?"0":"1")+r; n/=2;}
    return r;
}

int manhattanDistance(int x1,int x2,int y1,int y2) 
{
    return abs(x1-x2) + abs(y1-y2);
}

int euclidianDistance(int x1,int x2, int y1, int y2) 
{
    return sqrt(pow(x1-x2,2) + pow(y1-y2,2));
}

int hammingDistance(int x1,int x2, int y1, int y2) 
{
    int max = 0;
    
    std::string sx1 = toBinary(x1);
    max = maxNumber(max,sx1.length());
    std::string sx2 = toBinary(x2);
    max = maxNumber(max,sx2.length());
    std::string sy1 = toBinary(y1);
    max = maxNumber(max,sy1.length());
    std::string sy2 = toBinary(y2);
    max = maxNumber(max,sy2.length());
    
    sx1 = addZeros(sx1,max);
    sx2 = addZeros(sx2,max);
    sy1 = addZeros(sy1,max);
    sy2 = addZeros(sy2,max);
 
    int x = 0;
    int y = 0;
    
    for (int i = 0; i < sx1.length() && i < sx2.length(); i++) 
        if (sx1.at(i) != sx2.at(i)) 
            x++;
        
    
    for (int i = 0; i < sy1.length() && i < sy2.length(); i++) 
        if (sy1.at(i) != sy2.at(i)) 
            y++;
        
    
    
    return x - y;
}

int main()
{
    int x1,y1,x2,y2;
    
    std::cin >> x1 >> y1 >> x2 >> y2;
    std::cout << "Manhattan distance between: (" << x1 << ", " << y1 << ") , (" << x2 << ", " << y2 << ") : " << manhattanDistance(x1,x2,y1,y2) << std::endl;
    std::cout << "Euclidian distance between: (" << x1 << ", " << y1 << ") , (" << x2 << ", " << y2 << ") : " << euclidianDistance(x1,x2,y1,y2) << std::endl;
    std::cout << "Hamming distance between:   (" << x1 << ", " << y1 << ") , (" << x2 << ", " << y2 << ") : " << hammingDistance(x1,x2,y1,y2) << std::endl;

    return 0;
}