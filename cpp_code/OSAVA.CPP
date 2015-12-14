// OSAVA

#include <iostream>
#include <cmath>
using namespace std;

#include "OSAVA1.cpp"
#include "OSAVA2.cpp"
#include "OSAVA3.cpp"
#include "OSAVA4.cpp"
#include "OSAVA5.cpp"
#include "OSAVA6.cpp"

int main()
{int ch;
 do{cout<<"OSAVA\n"
	<<"1. CPU Scheduling Algorithms\n"
	<<"2. Deadlock Avaidance Algorithm\n"
	<<"3. Deadlock Detection Algorithm\n"
	<<"4. Contiguous Memory Allocation Algorithms\n"
	<<"5. Page Replacement Algorithms\n"
	<<"6. Disk Scheduling Algorithms\n"
	<<"7. Exit\n"
	<<"Enter choice: ";
    cin>>ch;
    switch(ch)
	{case 1:osava1();
		break;
	 case 2:osava2();
		break;
	 case 3:osava3();
		break;
	 case 4:osava4();
		break;
	 case 5:osava5();
		break;
	 case 6:osava6();
	}
   }while((ch>=1)&&(ch<=6));
}