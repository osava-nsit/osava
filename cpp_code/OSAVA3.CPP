// Deadlock Detection Algorithm

void osava3()
{int N,M,Available[10],Allocation[10][10],Work[10],Finish[10],Request[10][10];
 int i,j,k,complete,flag1,flag2;


 // INPUT
 cout<<"Enter number of processes (up to 10): ";
 cin>>N;
 cout<<"Enter number of resource types (up to 10): ";
 cin>>M;
 cout<<"Enter Available: ";
 for(j=0;j<M;j++)
	cin>>Available[j];
 cout<<"Enter Allocation:\n";
 for(i=0;i<N;i++)
	 for(j=0;j<M;j++)
		cin>>Allocation[i][j];
 cout<<"Enter Request:\n";
 for(i=0;i<N;i++)
	 for(j=0;j<M;j++)
		cin>>Request[i][j];
 cout<<"Deadlock Detection Algorithm: This algorithm examines the state of the system and determines whether a deadlock has occurred.\n";

 // SIMULATION
 for(j=0;j<M;j++)
	Work[j]=Available[j];
 for(i=0;i<N;i++)
	{Finish[i]=1;
	 for(j=0;j<M;j++)
		if(Allocation[i][j]!=0)
			{Finish[i]=0;
			 break;
			}
	}
 complete=0;
 cout<<"Initially - Work: [";
 for(j=0;j<M;j++)
	cout<<Work[j]<<" ";
 cout<<"\b] Finish: [";
 for(k=0;k<N;k++)
	if(Finish[k])
		cout<<"T ";
	else
		cout<<"F ";
 cout<<"\b]\n";
 while(!complete)
	{complete=1;
	 for(i=0;i<N;i++)
		{flag1=1;
		 for(j=0;j<M;j++)
			if(Request[i][j]>Work[j])
				{flag1=0;
				 break;
				}
		 if((Finish[i]==0)&&(flag1))
			{for(j=0;j<M;j++)
				Work[j]+=Allocation[i][j];
			 Finish[i]=1;
			 complete=0;
			 cout<<"P"<<i+1<<" selected - Work: [";
			 for(j=0;j<M;j++)
				cout<<Work[j]<<" ";
			 cout<<"\b] Finish: [";
			 for(k=0;k<N;k++)
				if(Finish[k])
					cout<<"T ";
				else
					cout<<"F ";
			 cout<<"\b]\n";
			}
		}
	}
 flag1=1;
 for(i=0;i<N;i++)
	if(Finish[i]==0)
		{flag1=0;
		 break;
		}
 if(flag1)
	cout<<"No deadlock detected.\n";
 else
	{cout<<"Deadlock detected.\n";
	 cout<<"Deadlocked processes: ";
	 for(i=0;i<N;i++)
		if(Finish[i]==0)
			cout<<"P"<<i+1<<", ";
	 cout<<"\b\b\n.";
	}

 // getch();
}