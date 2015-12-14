// Disk Scheduling Algorithms

void osava6()
{int N,Queue[100],Size,Start_pos,Start_dir,Algo,NC;
 int i,j,k,select,count,prev_pos,curr_pos,first,last;


 // INPUT
 cout<<"Enter number of cylinders (up to 1000): ";
 cin>>N;
 cout<<"Enter size of pending queue (up to 100): ";
 cin>>Size;
 cout<<"Enter pending queue: ";
 for(i=0;i<Size;i++)
	cin>>Queue[i];
 cout<<"Enter initial position of the r/w head: ";
 cin>>Start_pos;
 cout<<"Disk Scheduling Algorithms -"
     <<"\n1. First Come First Served Scheduling"
     <<"\n2. Shortest Seek Time First Scheduling"
     <<"\n3. SCAN Scheduling"
     <<"\n4. C-SCAN Scheduling"
     <<"\n5. LOOK Scheduling"
     <<"\n6. C-LOOK Scheduling"
     <<"\nEnter choice: ";
 cin>>Algo;
 if((Algo>=3)&&(Algo<=6))
	{cout<<"Enter initial direction of movement of the r/w head (1: Inward, 2: Outward): ";
	 cin>>Start_dir;
	}


 // SIMULATION
 switch(Algo)
	{case 1:cout<<"In First Come First Served Scheduling, the i/o requests are processed in the order in which they arrive.\n";
		break;
	 case 2:cout<<"In Shortest Seek Time First Scheduling, the i/o request which will need the minimum seek time is processed first.\n";
		break;
	 case 3:cout<<"In SCAN scheduling, the r/w head scans back and forth across the disk servicing requests as it reaches each cylinder.\n";
		break;
	 case 4:cout<<"In C-SCAN scheduling, the r/w head scans back and forth across the disk servicing requests as it reaches each cylinder. On reaching the end, the r/w head immediately returns to the beginning without servicing any request on the return trip.\n";
		break;
	 case 5:cout<<"In LOOK scheduling, the r/w head scans back and forth across the disk servicing requests as it reaches each cylinder moving only up to last requested cylinder in the given direction.\n";
		break;
	 case 6:cout<<"In C-LOOK Scheduling, the r/w head scans back and forth across the disk servicing requests as it reaches each cylinder moving only up to last requested cylinder in the given direction. On reaching the end, the r/w head immediately returns to the beginning, if need be, without servicing any request on the return trip.\n";
	}

 if(Algo==1)
	{cout<<"Path of the r/w head: "<<Start_pos;
	 curr_pos=Start_pos;
	 NC=0;
	 for(i=0;i<Size;i++)
		{prev_pos=curr_pos;
		 curr_pos=Queue[i];
		 cout<<"->"<<curr_pos;
		 NC+=abs(curr_pos-prev_pos);
		}
	 cout<<".\n";
	 cout<<"Number of cylinders travelled: "<<NC<<".\n";
	}
 else
 if(Algo==2)
	{cout<<"Path of the r/w head: "<<Start_pos;
	 curr_pos=Start_pos;
	 count=0;
	 NC=0;
	 while(count<Size)
		{for(i=0;i<Size;i++)
			if(Queue[i]!=-1)
				{select=i;
				 break;
				}
		 for(;i<Size;i++)
			if((Queue[i]!=-1)&&(abs(Queue[i]-curr_pos)<abs(Queue[select]-curr_pos)))
				select=i;
		 prev_pos=curr_pos;
		 curr_pos=Queue[select];
		 Queue[select]=-1;
		 cout<<"->"<<curr_pos;
		 NC+=abs(curr_pos-prev_pos);
		 count++;
		}
	 cout<<".\n";
	 cout<<"Number of cylinders travelled: "<<NC<<".\n";
	}
 else
 if(Algo==3)
	{cout<<"Path of the r/w head: "<<Start_pos;
	 curr_pos=Start_pos;
	 count=0;
	 NC=0;
	 if(Start_dir==1)
		{for(j=Start_pos;j<N;j++)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 Queue[i]=-1;
					 cout<<"->"<<curr_pos;
					 count++;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		 if(count<Size)
			{prev_pos=curr_pos;
			 curr_pos=N-1;
			 cout<<"->("<<curr_pos<<")";
			 NC+=abs(curr_pos-prev_pos);
			}
		 for(j=N;j>=0;j--)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 cout<<"->"<<curr_pos;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		}
	 else
		{for(j=Start_pos;j>=0;j--)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 Queue[i]=-1;
					 cout<<"->"<<curr_pos;
					 count++;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		 if(count<Size)
			{prev_pos=curr_pos;
			 curr_pos=0;
			 cout<<"->("<<curr_pos<<")";
			 NC+=abs(curr_pos-prev_pos);
			}
		 for(j=0;j<N;j++)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 cout<<"->"<<curr_pos;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		}
	 cout<<".\n";
	 cout<<"Number of cylinders travelled: "<<NC<<".\n";
	}
 else
 if(Algo==4)
	{cout<<"Path of the r/w head: "<<Start_pos;
	 curr_pos=Start_pos;
	 count=0;
	 NC=0;
	 if(Start_dir==1)
		{for(j=Start_pos;j<N;j++)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 cout<<"->"<<curr_pos;
					 count++;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		 if(count<Size)
			{prev_pos=curr_pos;
			 curr_pos=N-1;
			 cout<<"->("<<curr_pos<<")";
			 NC+=abs(curr_pos-prev_pos);
			 prev_pos=curr_pos;
			 curr_pos=0;
			 cout<<"->("<<curr_pos<<")";
			 NC++;
			}
		 for(j=0;j<Start_pos;j++)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 cout<<"->"<<curr_pos;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		}
	 else
		{for(j=Start_pos;j>=0;j--)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 cout<<"->"<<curr_pos;
					 count++;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		 if(count<Size)
			{prev_pos=curr_pos;
			 curr_pos=0;
			 cout<<"->("<<curr_pos<<")";
			 NC+=abs(curr_pos-prev_pos);
			 prev_pos=curr_pos;
			 curr_pos=N-1;
			 cout<<"->("<<curr_pos<<")";
			 NC++;
			}
		 for(j=N-1;j>Start_pos;j--)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 cout<<"->"<<curr_pos;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		}
	 cout<<".\n";
	 cout<<"Number of cylinders travelled: "<<NC<<".\n";
	}
 else
 if(Algo==5)
	{cout<<"Path of the r/w head: "<<Start_pos;
	 curr_pos=Start_pos;
	 NC=0;
	 if(Start_dir==1)
		{for(j=Start_pos;j<N;j++)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 Queue[i]=-1;
					 cout<<"->"<<curr_pos;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		 for(j=N;j>=0;j--)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 cout<<"->"<<curr_pos;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		}
	 else
		{for(j=Start_pos;j>=0;j--)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 Queue[i]=-1;
					 cout<<"->"<<curr_pos;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		 for(j=0;j<N;j++)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 cout<<"->"<<curr_pos;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		}
	 cout<<".\n";
	 cout<<"Number of cylinders travelled: "<<NC<<".\n";
	}
 else
 if(Algo==6)
	{cout<<"Path of the r/w head: "<<Start_pos;
	 curr_pos=Start_pos;
	 count=0;
	 NC=0;
	 if(Start_dir==1)
		{for(j=Start_pos;j<N;j++)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 Queue[i]=-1;
					 cout<<"->"<<curr_pos;
					 count++;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		 if(count<Size)
			{first=-1;
			 for(k=0;k<Start_pos;k++)
				{for(i=0;i<Size;i++)
					if(Queue[i]==k)
						{first=k;
						 break;
						}
				 if(first!=-1)
					break;
				}
			 last=-1;
			 for(k=Start_pos-1;k>-0;k--)
				{for(i=0;i<Size;i++)
					if(Queue[i]==k)
						{last=k;
						 break;
						}
				 if(last!=-1)
					break;
				}
			 if(N-curr_pos+first<curr_pos-last)
				{prev_pos=curr_pos;
				 curr_pos=N-1;
				 cout<<"->("<<curr_pos<<")";
				 NC+=abs(curr_pos-prev_pos);
				 prev_pos=curr_pos;
				 curr_pos=0;
				 cout<<"->("<<curr_pos<<")";
				 NC++;
				 for(j=0;j<Start_pos;j++)
					for(i=0;i<Size;i++)
						if(Queue[i]==j)
							{prev_pos=curr_pos;
							 curr_pos=j;
							 cout<<"->"<<curr_pos;
							 NC+=abs(curr_pos-prev_pos);
							 break;
							}
				}
			 else
				{for(j=N;j>=0;j--)
					for(i=0;i<Size;i++)
					if(Queue[i]==j)
						{prev_pos=curr_pos;
						 curr_pos=j;
						 cout<<"->"<<curr_pos;
						 NC+=abs(curr_pos-prev_pos);
						 break;
						}
				}
			}
		}
	 else
		{for(j=Start_pos;j>=0;j--)
			for(i=0;i<Size;i++)
				if(Queue[i]==j)
					{prev_pos=curr_pos;
					 curr_pos=j;
					 Queue[i]=-1;
					 cout<<"->"<<curr_pos;
					 count++;
					 NC+=abs(curr_pos-prev_pos);
					 break;
					}
		 if(count<Size)
			{first=-1;
			 for(k=Start_pos+1;k<N;k++)
				{for(i=0;i<Size;i++)
					if(Queue[i]==k)
						{first=k;
						 break;
						}
				 if(first!=-1)
					break;
				}
			 last=-1;
			 for(k=N-1;k>Start_pos;k--)
				{for(i=0;i<Size;i++)
					if(Queue[i]==k)
						{last=k;
						 break;
						}
				 if(last!=-1)
					break;
				}
			 if(curr_pos+N-last<first-curr_pos)
				{prev_pos=curr_pos;
				 curr_pos=0;
				 cout<<"->("<<curr_pos<<")";
				 NC+=abs(curr_pos-prev_pos);
				 prev_pos=curr_pos;
				 curr_pos=N-1;
				 cout<<"->("<<curr_pos<<")";
				 NC++;
				 for(j=N-1;j>Start_pos;j--)
					for(i=0;i<Size;i++)
						if(Queue[i]==j)
							{prev_pos=curr_pos;
							 curr_pos=j;
							 cout<<"->"<<curr_pos;
							 NC+=abs(curr_pos-prev_pos);
							 break;
							}
				}
			 else
				{for(j=0;j<N;j++)
					for(i=0;i<Size;i++)
						if(Queue[i]==j)
							{prev_pos=curr_pos;
							 curr_pos=j;
							 cout<<"->"<<curr_pos;
							 NC+=abs(curr_pos-prev_pos);
							 break;
							}
				}
			}
		}
	 cout<<".\n";
	 cout<<"Number of cylinders travelled: "<<NC<<".\n";
	}

 // getch();
}