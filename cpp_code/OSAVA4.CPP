// Contiguous Memory Allocation Algorithms

struct _process
{int id, // 1 to 25
     size, // in KB
     arrival_time,
     termination_time;
};

struct memory_slot
{int pid, // 0: hole, Otherwise: valid process
     starting_addr,
     size;
};

void osava4()
{_process P[25];
 memory_slot S[26];
 int N,M,Size,Algo,T,Complete;
 int i,j,k,flag,size,sum,select;


 // INPUT
 cout<<"Enter number of processes (up to 25): ";
 cin>>N;
 for(i=0;i<N;i++)
	{P[i].id=i+1;
	 cout<<"P"<<P[i].id<<" -\n";
	 cout<<"\tSize (KB): ";
	 cin>>P[i].size;
	 cout<<"\tArrival time: ";
	 cin>>P[i].arrival_time;
	 cout<<"\tTermination time: ";
	 cin>>P[i].termination_time;
	}
 cout<<"Enter size of main memory (KB): ";
 cin>>Size;
 cout<<"Contiguous Memory Allocation Algorithms -"
     <<"\n1. First Fit Algorithm"
     <<"\n2. Best Fit Algorithm"
     <<"\n3. Worst Fit Algorithm"
     <<"\nEnter choice: ";
 cin>>Algo;


 // SIMULATION
  switch(Algo)
	{case 1:cout<<"In the First Fit Algorithm, a process is loaded in the first hole that is large enough for the process to be found.\n";
		break;
	 case 2:cout<<"In the Best Fit Algorithm, a process is loaded in the smallest hole that is large enough for the process.\n";
		break;
	 case 3:cout<<"In the Worst Fit Algorithm, a process is loaded in the largest hole.\n";
	}

 T=0;
 Complete=0;
 M=1;
 S[0].pid=0;
 S[0].starting_addr=0;
 S[0].size=Size;
 flag=0;
 cout<<"Main memory at "<<T<<" ms -\n";
 for(j=0;j<M;j++)
	{cout<<"\t"<<S[j].starting_addr<<"-"
	     <<S[j].starting_addr+S[j].size-1<<": ";
	 if(S[j].pid)
		cout<<"P"<<S[j].pid<<".\n";
	 else
		cout<<"Hole.\n";
	 // getch();
	}
 while(!Complete)
	{for(i=0;i<N;i++)
		if(P[i].termination_time==T)
			{for(j=0;j<M;j++)
				if(S[j].pid==P[i].id)
					{S[j].pid=0;
					 break;
					}
			 for(j=0;j<M-1;j++)
				if((S[j].pid==0)&&(S[j+1].pid==0))
					{S[j].size+=S[j+1].size;
					 for(k=j+1;k<M-1;k++)
						S[k]=S[k+1];
					 M--;
					 break;
					}
			 for(j=0;j<M-1;j++)
				if((S[j].pid==0)&&(S[j+1].pid==0))
					{S[j].size+=S[j+1].size;
					 for(k=j+1;k<M-1;k++)
						S[k]=S[k+1];
					 M--;
					 break;
					}
			 P[i].size=-1;
			 flag=1;
			}
	 for(i=0;i<N;i++)
		if(P[i].arrival_time==T)
			{// First Fit Algorithm
			 if(Algo==1)
				 {for(j=0;j<M;j++)
					if((S[j].pid==0)&&(S[j].size>=P[i].size))
						{for(k=M;k>j;k--)
							S[k]=S[k-1];
						 M++;
						 S[j].pid=P[i].id;
						 S[j+1].size=S[j].size-P[i].size;
						 S[j].size=P[i].size;
						 S[j+1].starting_addr=S[j].starting_addr+S[j].size;
						 flag=1;
						 break;
						}
				 }
			 else
			 // Best Fit Algorithm
			 if(Algo==2)
				 {select=-1;
				  for(j=0;j<M;j++)
					if((S[j].pid==0)&&(S[j].size>=P[i].size))
						{select=j;
						 break;
						}
				  for(;j<M;j++)
					if((S[j].pid==0)&&(S[j].size>=P[i].size)&&(S[j].size<S[select].size))
						select=j;
				  if(select!=-1)
					{for(k=M;k>select;k--)
							S[k]=S[k-1];
					 M++;
					 S[select].pid=P[i].id;
					 S[select+1].size=S[select].size-P[i].size;
					 S[select].size=P[i].size;
					 S[select+1].starting_addr=S[select].starting_addr+S[select].size;
					 flag=1;
					}
				 }
			 else
			 // Worst Fit Algorithm
			 if(Algo==3)
				 {select=-1;
				  for(j=0;j<M;j++)
					if((S[j].pid==0)&&(S[j].size>=P[i].size))
						{select=j;
						 break;
						}
				  for(;j<M;j++)
					if((S[j].pid==0)&&(S[j].size>=P[i].size)&&(S[j].size>S[select].size))
						select=j;
				  if(select!=-1)
					{for(k=M;k>select;k--)
							S[k]=S[k-1];
					 M++;
					 S[select].pid=P[i].id;
					 S[select+1].size=S[select].size-P[i].size;
					 S[select].size=P[i].size;
					 S[select+1].starting_addr=S[select].starting_addr+S[select].size;
					 flag=1;
					}
				 }
			 if(!flag)
				{sum=0;
				 for(j=0;j<M;j++)
					if(S[j].pid==0)
						sum+=S[j].size;
				 if(P[i].size>sum)
					cout<<"At "<<T<<" ms, P"<<P[i].id<<" cannot be loaded because not enough free memory is available.\n";
				 else
					cout<<"At "<<T<<" ms, P"<<P[i].id<<" cannot be loaded because of external fragmentation though enough free memory is available.\n";
				 Complete=1;
				 // getch();
				}
		       }
	 if(flag)
		{cout<<"Main memory at "<<T<<" ms -\n";
		 for(j=0;j<M;j++)
			{cout<<"\t"<<S[j].starting_addr<<"-"
			    <<S[j].starting_addr+S[j].size-1<<": ";
			 if(S[j].pid)
				 cout<<"P"<<S[j].pid<<".\n";
			 else
				 cout<<"Hole.\n";
			}
		 flag=0;
		 // getch();
		}
	 if(!Complete)
		 {Complete=1;
		 for(i=0;i<N;i++)
			if(P[i].size!=-1)
				{Complete=0;
				 break;
				}
		 }
	 T++;
	}
}