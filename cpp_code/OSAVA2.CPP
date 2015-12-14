// Deadlock Avaidance Algorithm

void osava2()
{int N,M,Available[10],Max[10][10],Allocation[10][10],Need[10][10],
     Work[10],Finish[10],P,Request[10],Sequence[10];
 int i,j,k,l,complete,flag1,flag2;


 // INPUT
 cout<<"Enter number of processes (up to 10): ";
 cin>>N;
 cout<<"Enter number of resource types (up to 10): ";
 cin>>M;
 cout<<"Enter Available: ";
 for(j=0;j<M;j++)
	cin>>Available[j];
 cout<<"Enter Max:\n";
 for(i=0;i<N;i++)
	 for(j=0;j<M;j++)
		cin>>Max[i][j];
 cout<<"Enter Allocation:\n";
 for(i=0;i<N;i++)
	 for(j=0;j<M;j++)
		cin>>Allocation[i][j];
 cout<<"Enter process making request (1 to "<<N<<"): ";
 cin>>P;
 P--;
 cout<<"Enter Request: ";
 for(j=0;j<M;j++)
	cin>>Request[j];
 cout<<"Banker's Algorithm: When a process requests a set of resources, the system must determine whether granting the request will keep the system in a safe state.\n";

 // RESOURCE-REQUEST ALGORITHM
 cout<<"Resource-Request Algorithm -\n";
 for(i=0;i<N;i++)
	for(j=0;j<M;j++)
		Need[i][j]=Max[i][j]-Allocation[i][j];
 for(j=0;j<M;j++)
	if(Request[j]>Need[P][j])
		{cout<<"Error: P"<<P+1<<" requesting more resource than it needs.\n";
		 return;
		}
 for(j=0;j<M;j++)
	if(Request[j]>Available[j])
		{cout<<"Wait: P"<<P+1<<" requesting more resource than currently available.\n";
		 return;
		}
 cout<<"If the request is granted then the system will be in the following state -\n";
 for(j=0;j<M;j++)
	Available[j]-=Request[j];
 for(j=0;j<M;j++)
	Allocation[P][j]+=Request[j];
 for(j=0;j<M;j++)
	Need[P][j]-=Request[j];
 cout<<"Available: ";
 for(j=0;j<M;j++)
	cout<<Available[j]<<" ";
 cout<<"\n";
 cout<<"Allocation:\n";
 for(i=0;i<N;i++)
	{for(j=0;j<M;j++)
		cout<<Allocation[i][j]<<" ";
	 cout<<"\n";
	}
 cout<<"Need:\n";
 for(i=0;i<N;i++)
	{for(j=0;j<M;j++)
		cout<<Need[i][j]<<" ";
	 cout<<"\n";
	}


 // SAFETY ALGORITHM
 cout<<"Safety Algorithm -\n";
 for(j=0;j<M;j++)
	Work[j]=Available[j];
 for(i=0;i<N;i++)
	Finish[i]=0;
 complete=0;
 l=0;
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
			if(Need[i][j]>Work[j])
				{flag1=0;
				 break;
				}
		 if((Finish[i]==0)&&(flag1))
			{for(j=0;j<M;j++)
				Work[j]+=Allocation[i][j];
			 Finish[i]=1;
			 Sequence[l++]=i;
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
	{cout<<"Safe sequence: <";
	 for(k=0;k<l;k++)
		cout<<"P"<<Sequence[k]+1<<",";
	 cout<<"\b>\n";
	 cout<<"Safe state: Request should be granted.\n";
	}
 else
	cout<<"Unsafe state: Request should not be granted.\n";

 // getch();
}