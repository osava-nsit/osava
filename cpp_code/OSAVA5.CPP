// Page Replacement Algorithms

// Header files
// #include<iostream.h>
// #include<conio.h>

struct sca_queue_element
{int page,reference_bit;
};

struct esca_queue_element
{int page,reference_bit,modify_bit;
};

void osava5()
{int M,N,RS[100],RO[100],Frames[10],Algo,Count;
 int Queue1[10];
 sca_queue_element Queue2[11];
 esca_queue_element Queue3[10];
 int Queue_size;
 int Usage[10];
 char ch;
 int i,j,k,flag1,flag2,select;
 // flag1 - 1: Page available in memory, 0: Otherwise
 // flag2 - 1: Empty frame available in memory, 0: Otherwise


 // INPUT

 cout<<"Enter number of frames (up to 10): ";
 cin>>M;
 cout<<"Enter size of reference string (up to 100): ";
 cin>>N;
 cout<<"Enter reference string: ";
 for(i=0;i<N;i++)
	cin>>RS[i];
 cout<<"Page Replacement Algorithms -"
     <<"\n1. First In First Out Page Replacement Algorithm"
     <<"\n2. Optimal Page Replacement Algorithm"
     <<"\n3. Least Recently Used Page Replacement Algorithm"
     <<"\n4. Second Chance Page Replacement Algorithm"
     <<"\n5. Enhanced Second Chance Page Replacement Algorithm"
     <<"\n6. Least Frequently Used Page Replacement Algorithm"
     <<"\n7. Most Frequently Used Page Replacement Algorithm"
     <<"\nEnter choice: ";
 cin>>Algo;
 if(Algo==5)
	for(i=0;i<N;i++)
		{cout<<"Is the reference to Page "<<RS[i]<<" a read-only access (Y/N)? ";
		 cin>>ch;
		 if((ch=='Y')||(ch=='y'))
			RO[i]=1;
		 else
			RO[i]=0;
		}


 // SIMULATION

 switch(Algo)
	{case 1:cout<<"In First In First Out Page Replacement Algorithm, the page that was loaded earliest in the memory is replaced.\n";
		break;
	 case 2:cout<<"In Optimal Page Replacement Algorithm, the page that will not be referenced for the longest period of time is replaced.\n";
		break;
	 case 3:cout<<"In Least Recently Used Page Replacement Algorithm, the page that has not been referenced for the longest period of time is replaced.\n";
		break;
	 case 4:cout<<"In Second Chance Page Replacement Algorithm, the page that was loaded earliest in the memory is replaced. However, if the reference bit of the page is set then that page is given a second chance and the next possible page is replaced. When a page is given a second chance, its reference bit is reset and its arrival time is set to the current time.\n";
		break;
	 case 5:cout<<"In Enhanced Second Chance Page Replacement Algorithm, the pages are divided in four classes using their reference bit and modify bit as ordered pairs. The page of the lowest nonempty class which was loaded earliest in the memory is replaced.\n";
		break;
	 case 6:cout<<"In Least Frequently Used Page Replacement Algorithm, the page that has been referenced the least number of times is replaced.\n";
		break;
	 case 7:cout<<"In Most Frequently Used Page Replacement Algorithm, the page that has been referenced the most number of times is replaced.\n";
	}

 Queue_size=0;
 Count=0;
 for(j=0;j<M;j++)
	Frames[j]=-1;
 for(i=0;i<N;i++)
	{cout<<"Page "<<RS[i]<<" referenced: ";
	 flag1=0;
	 flag2=0;
	 for(j=0;j<M;j++)
		if(Frames[j]==RS[i]) // Page available in memory
			{flag1=1;
			 if(Algo==4)
				 for(k=0;k<Queue_size;k++)
					{if(Queue2[k].page==Frames[j])
						{Queue2[k].reference_bit=1;
						 break;
						}
					}
			 else
			 if(Algo==5)
				 for(k=0;k<Queue_size;k++)
					if(Queue3[k].page==Frames[j])
						{if(RO[i])
							Queue3[k].reference_bit=1;
						 else
							Queue3[k].modify_bit=1;
						 break;
						}
			 break;
			}
		else
		if(Frames[j]==-1) // Empty frame available in memory
			{Frames[j]=RS[i];
			 if(Algo==1)
				Queue1[Queue_size++]=RS[i];
			 else
			 if(Algo==4)
				{Queue2[Queue_size].page=RS[i];
				 Queue2[Queue_size++].reference_bit=0;
				}
			 else
			 if(Algo==5)
				{Queue3[Queue_size].page=RS[i];
				 if(RO[i])
					{Queue3[Queue_size].reference_bit=1;
					 Queue3[Queue_size++].modify_bit=0;
					}
				 else
					{Queue3[Queue_size].reference_bit=0;
					 Queue3[Queue_size++].modify_bit=1;
					}
				}
			 flag2=1;
			 Count++;
			 break;
			}
	 if(!flag1&&!flag2) // Page replacement
		{if(Algo==1)
			{for(j=0;j<M;j++)
				if(Frames[j]==Queue1[0])
					{Frames[j]=RS[i];
					 break;
					}
			 for(k=0;k<Queue_size-1;k++)
				Queue1[k]=Queue1[k+1];
			 Queue1[Queue_size-1]=RS[i];
			}
		 else
		 if(Algo==2)
			{// Usage[j]: Next access to the page in Frames[j]
			 for(j=0;j<M;j++)
				Usage[j]=N;
			 for(k=N-1;k>i;k--)
				for(j=0;j<M;j++)
					if(RS[k]==Frames[j])
						{Usage[j]=k;
						 break;
						}
			 select=0;
			 for(j=1;j<M;j++)
				if(Usage[j]>Usage[select])
					select=j;
			 Frames[select]=RS[i];
			}
		 else
		 if(Algo==3)
			{// Usage[j]: Last access to the page in Frames[j]
			 for(j=0;j<M;j++)
				Usage[j]=-1;
			 for(k=0;k<i;k++)
				for(j=0;j<M;j++)
					if(RS[k]==Frames[j])
						{Usage[j]=k;
						 break;
						}
			 select=0;
			 for(j=1;j<M;j++)
				if(Usage[j]<Usage[select])
					select=j;
			 Frames[select]=RS[i];
			}
		 else
		 if(Algo==4)
			{while(Queue2[0].reference_bit)
				{Queue2[0].reference_bit=0;
				 Queue2[Queue_size]=Queue2[0];
				 for(k=0;k<Queue_size;k++)
					Queue2[k]=Queue2[k+1];
				}
			 for(j=0;j<M;j++)
				if(Frames[j]==Queue2[0].page)
					{Frames[j]=RS[i];
					 break;
					}
			 for(k=0;k<Queue_size-1;k++)
				Queue2[k]=Queue2[k+1];
			 Queue2[Queue_size-1].page=RS[i];
			 Queue2[Queue_size-1].reference_bit=0;
			}
		 else
		 if(Algo==5)
			{select=-1;
			 for(k=0;k<Queue_size;k++)
				if(!Queue3[k].reference_bit&&!Queue3[k].modify_bit)
					{select=k;
					 break;
					}
			 if(select==-1)
				 for(k=0;k<Queue_size;k++)
					if(!Queue3[k].reference_bit&&Queue3[k].modify_bit)
						{select=k;
						 break;
						}
			 if(select==-1)
				 for(k=0;k<Queue_size;k++)
					if(Queue3[k].reference_bit&&!Queue3[k].modify_bit)
						{select=k;
						 break;
						}
			 if(select==-1)
				 for(k=0;k<Queue_size;k++)
					if(Queue3[k].reference_bit&&Queue3[k].modify_bit)
						{select=k;
						 break;
						}
			 for(j=0;j<M;j++)
				if(Frames[j]==Queue3[select].page)
					{Frames[j]=RS[i];
					 break;
					}
			 for(k=select;k<Queue_size-1;k++)
				Queue3[k]=Queue3[k+1];
			 Queue3[Queue_size-1].page=RS[i];
			 if(RO[i])
				{Queue3[Queue_size-1].reference_bit=1;
				 Queue3[Queue_size-1].modify_bit=0;
				}
			 else
				{Queue3[Queue_size-1].reference_bit=0;
				 Queue3[Queue_size-1].modify_bit=1;
				}
			}
		 else
		 if(Algo==6)
			{// Usage[j]: Number of accesses to the page in Frames[j]
			 for(j=0;j<M;j++)
				Usage[j]=0;
			 for(k=0;k<i;k++)
				for(j=0;j<M;j++)
					if(RS[k]==Frames[j])
						{Usage[j]++;
						 break;
						}
			 select=0;
			 for(j=1;j<M;j++)
				if(Usage[j]<Usage[select])
					select=j;
			 Frames[select]=RS[i];
			}
		 else
		 if(Algo==7)
			{// Usage[j]: Number of accesses to the page in Frames[j]
			 for(j=0;j<M;j++)
				Usage[j]=0;
			 for(k=0;k<i;k++)
				for(j=0;j<M;j++)
					if(RS[k]==Frames[j])
						{Usage[j]++;
						 break;
						}
			 select=0;
			 for(j=1;j<M;j++)
				if(Usage[j]>Usage[select])
					select=j;
			 Frames[select]=RS[i];
			}
		 Count++;
		}
	 for(j=0;j<M;j++)
		if(Frames[j]==-1)
			cout<<"x ";
		else
			cout<<Frames[j]<<" ";
	 if(!flag1||flag2)
		cout<<"[Page fault]";
	 cout<<"\n";
	}
 cout<<"Number of page faults: "<<Count<<"\n";

 // getch();
}