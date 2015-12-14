// CPU Scheduling Algorithms

// Information about a queue of Algos. 5 and 6
struct queue_info
{int algo,tq;
};

// A process
struct process
{char name[4];
 int arrival_time,cpu_burst_time,priority,queue_assigned,
     response_time,waiting_time,waiting_since,time_required,
     tq_left,termination_time;
};

void osava1()
{process P[25]; // The set of processes
 int N, // Number of processes
     Algo, // CPU scheduling algorithm being used
     Var, // 1: Non-preemptive, 2: Preemptive
     Aging, // 1: Use aging, 0: Otherwise
     Aging_Q, // Time duration for aging
     Aging_L, // Aging priority limit
     TQ, // Time quantum
     TQ_left, // Time quantum remaining
     NQ, // Number of queues
     DL, // Dispatch latency
     DL_left, // Dispatch latency time remaining
     RUNNING, // The running process
     Just_idle, // 1: Just became idle, 0: Otherwise
     Just_dl, // 1: Just started dispatch latency, 0: Otherwise
     T, // Simulation time
     COMPLETE; // 1: Simulation complete, 0: Otherwise
 queue_info QI[10]; // Multiple queues
 char ch; // Temporary variables
 int i,sum,temp,select,
     select_arrival_time,select_cpu_burst_time,select_priority; // Temporary variables
 float mean,sd; // Temporary variables


 // INPUT **********************************************************************

 cout<<"Enter number of processes (1 to 25): ";
 cin>>N;

 for(i=0;i<N;i++)
	{P[i].name[0]='P';
	 if(i<9)
		{P[i].name[1]='0'+i+1;
		 P[i].name[2]='\0';
		}
	 else
		{P[i].name[1]='0'+(i+1)/10;
		 P[i].name[2]='0'+(i+1)%10;
		 P[i].name[3]='\0';
		}
	 cout<<P[i].name<<":\n";
	 cout<<"\tEnter arrival time (ms): ";
	 cin>>P[i].arrival_time;
	 cout<<"\tEnter CPU burst time (ms): ";
	 cin>>P[i].cpu_burst_time;
	 P[i].response_time=P[i].waiting_since=P[i].termination_time=-1;
	 P[i].waiting_time=0;
	 P[i].time_required=P[i].cpu_burst_time;
	}

 cout<<"CPU Scheduling Algorithms -"
     <<"\n1. First Come First Served Scheduling"
     <<"\n2. Shortest Job First Scheduling"
     <<"\n3. Priority Scheduling"
     <<"\n4. Round Robin Scheduling"
     <<"\n5. Multilevel Queue Scheduling"
     <<"\n6. Multilevel Feedback Queue Scheduling"
     <<"\nEnter choice: ";
 cin>>Algo;

 if((Algo==2)||(Algo==3))
	{cout<<"Variants -"
	     <<"\n1. Non-preemptive"
	     <<"\n2. Preemptive"
	     <<"\nEnter choice: ";
	 cin>>Var;
	}

 if(Algo==3)
	{cout<<"Enter priorities of processes (0 being the highest) -\n";
	 for(i=0;i<N;i++)
		{cout<<P[i].name<<": ";
		 cin>>P[i].priority;
		}
	 cout<<"Is the concept of aging being used (y/n)? ";
	 cin>>ch;
	 if((ch=='y')||(ch=='Y'))
		{Aging=1;
		 cout<<"After how much wait priority of a process is to be incremented (ms)? ";
		 cin>>Aging_Q;
		 cout<<"To what limit priority of a process can be incremented? ";
		 cin>>Aging_L;
		}
	 else
		Aging=0;
	}

 if(Algo==4)
	{cout<<"Enter time quantum (ms): ";
	 cin>>TQ;
	}

 if((Algo==5)||(Algo==6))
	{cout<<"Enter number of queues (2-10): ";
	 cin>>NQ;
	}

 if(Algo==5)
	{cout<<"Enter intra-queue scheduling algorithm (1. FCFS, 2: RR) -\n";
	 for(i=0;i<NQ;i++)
		{cout<<"Q"<<i+1<<": ";
		 cin>>QI[i].algo;
		 if(QI[i].algo==2)
			{cout<<"Enter time quantum (ms): ";
			 cin>>QI[i].tq;
			}
		}
	 cout<<"Enter the queues assigned -\n";
	 for(i=0;i<N;i++)
		{cout<<P[i].name<<": ";
		 cin>>P[i].queue_assigned;
		 P[i].queue_assigned--;
		}
	}

 if(Algo==6)
	{cout<<"Enter time quantum (ms) -\n";
	 for(i=0;i<NQ-1;i++)
		{cout<<"Q"<<i+1<<": ";
		 cin>>QI[i].tq;
		}
	 for(i=0;i<N;i++)
		P[i].queue_assigned=0;
	}

 cout<<"Enter dispatch latency (ms): ";
 cin>>DL;


 // SIMULATION ****************************************************************

 switch(Algo)
	{case 1:cout<<"In First Come First Served Scheduling, the processor is allocated to the process which has arrived first. It is a non-preemptive algorithm.\n";
		break;
	 case 2:cout<<"In Shortest Job First Scheduling, the processor is allocated to the process which has the shortest next CPU burst. It can be either preemptive or non-preemptive. Preemptive shortest job first scheduling is also known as shortest remaining time first scheduling.\n";
		break;
	 case 3:cout<<"In Priority Scheduling, the processor is allocated to the process which has the highest priority. It can be either preemptive or non-preemptive.\n";
		break;
	 case 4:cout<<"In Round Robin Scheduling, the processor is allocated to a process for a small time quantum. The processes are logically arranged in a circular queue. It is a preemptive algorithm.\n";
		break;
	 case 5:cout<<"In Multilevel Queue Scheduling, the ready queue is partitioned into several queues. A process is permanently assigned to a queue. Each queue has its own scheduling algorithm. Preemptive priority scheduling is often used for inter-queue scheduling.\n";
		break;
	 case 6:cout<<"In Multilevel Feedback Queue Scheduling, the ready queue is partitioned into several queues. The processes can move between the queues. Each queue has its own scheduling algorithm. Preemptive priority scheduling is typically used for inter-queue scheduling.\n";
	}

 T=0;
 COMPLETE=0;
 RUNNING=-1;
 Just_idle=1;
 cout<<"Timeline -\n";
 while(!COMPLETE)
 {// Aging
  if((Algo==3)&&(Aging))
	for(i=0;i<N;i++)
		if((P[i].arrival_time<=T)&&
		   (P[i].time_required>0)&&
		   (RUNNING!=i)&&
		   ((P[i].waiting_time+T-P[i].waiting_since)%Aging_Q==0)&&
		   (P[i].priority>Aging_L))
			{P[i].priority--;
			 cout<<T<<" ms: Priority of "<<P[i].name<<" increased to "<<P[i].priority<<".\n";
			}
  // Arrival
  for(i=0;i<N;i++)
	if(P[i].arrival_time==T)
		{P[i].waiting_since=T;
		 cout<<T<<" ms: "<<P[i].name<<" arrived.\n";
		 // Preemption
		 if(((Algo==2)&&(Var==2)&&(RUNNING>=0)&&(P[i].time_required<P[RUNNING].time_required-1))||
		    ((Algo==3)&&(Var==2)&&(RUNNING>=0)&&(P[i].priority<P[RUNNING].priority))||
		    ((Algo==5)&&(RUNNING>=0)&&(P[i].queue_assigned<P[RUNNING].queue_assigned))||
		    ((Algo==6)&&(RUNNING>=0)&&(P[i].queue_assigned<P[RUNNING].queue_assigned)))
			{P[RUNNING].time_required--;
			 P[RUNNING].waiting_since=T;
			 cout<<T<<" ms: "<<P[RUNNING].name<<" suspended.\n";
			 if(DL)
				{RUNNING=-2;
				 DL_left=DL;
				 Just_dl=1;
				}
			 else
				{RUNNING=-1;
				 Just_idle=1;
				}
			}
		}
  // Time quantum expired
  if((Algo==4)&&(TQ_left==0)&&(P[RUNNING].time_required>1))
	{temp=0;
	 for(i=0;i<N;i++)
		if((P[i].arrival_time<=T)&&(P[i].time_required>0))
			temp++;
	 if(temp==1)
		TQ_left=TQ;
	 else
		{P[RUNNING].time_required--;
		 P[RUNNING].waiting_since=T;
		 cout<<T<<" ms: "<<P[RUNNING].name<<" suspended.\n";
		 if(DL)
			{RUNNING=-2;
			 DL_left=DL;
			 Just_dl=1;
			}
		 else
			{RUNNING=-1;
			 Just_idle=1;
			}
		}
	}
  else
  if((Algo==5)&&(RUNNING>=0)&&(QI[P[RUNNING].queue_assigned].algo==2)&&(P[RUNNING].tq_left==0)&&(P[RUNNING].time_required>1))
	{temp=0;
	 for(i=0;i<N;i++)
		if((P[i].arrival_time<=T)&&(P[i].time_required>0)&&(P[i].queue_assigned==P[RUNNING].queue_assigned))
			temp++;
	 P[RUNNING].tq_left=QI[P[RUNNING].queue_assigned].tq;
	 if(temp>1)
		{P[RUNNING].time_required--;
		 P[RUNNING].waiting_since=T;
		 cout<<T<<" ms: "<<P[RUNNING].name<<" suspended.\n";
		 if(DL)
			{RUNNING=-2;
			 DL_left=DL;
			 Just_dl=1;
			}
		 else
			{RUNNING=-1;
			 Just_idle=1;
			}
		}
	}
  else
  if((Algo==6)&&(RUNNING>=0)&&(P[RUNNING].queue_assigned<NQ-1)&&(P[RUNNING].tq_left==0)&&(P[RUNNING].time_required>1))
	{P[RUNNING].queue_assigned++;
	 cout<<T<<" ms: "<<P[RUNNING].name<<" moved to Q"<<P[RUNNING].queue_assigned+1<<".\n";
	 temp=0;
	 for(i=0;i<N;i++)
		if((P[i].arrival_time<=T)&&(P[i].time_required>0))
			temp++;
	 P[RUNNING].tq_left=QI[P[RUNNING].queue_assigned].tq;
	 if(temp>1)
		{P[RUNNING].time_required--;
		 P[RUNNING].waiting_since=T;
		 cout<<T<<" ms: "<<P[RUNNING].name<<" suspended.\n";
		 if(DL)
			{RUNNING=-2;
			 DL_left=DL;
			 Just_dl=1;
			}
		 else
			{RUNNING=-1;
			 Just_idle=1;
			}
		}
	}
  // Dispatch latency
  if(RUNNING==-2)
	{if(Just_dl==1)
		{cout<<T<<" ms: Dispatch latency.\n";
		 Just_dl=0;
		}
	 DL_left--;
	 if(DL_left==0)
		{RUNNING=-1;
		 Just_idle=1;
		}
	}
  else
  // Idle
  if(RUNNING==-1)
	{temp=0;
	 for(i=0;i<N;i++)
		if((P[i].arrival_time<=T)&&(P[i].time_required>0))
			{temp=1;
			 break;
			}
	 // Idling
	 if(temp==0)
		{if(Just_idle==1)
			{cout<<T<<" ms: Idle.\n";
			 Just_idle=0;
			}
		}
	 // Starting or resumption
	 else
		{for(i=0;i<N;i++)
			if((P[i].arrival_time<=T)&&(P[i].time_required>0))
				{select=i;
				 break;
				}
		 if(Algo==1)
			for(;i<N;i++)
				{if((P[i].arrival_time<=T)&&
				    (P[i].time_required>0)&&
				    (P[i].arrival_time<P[select].arrival_time))
					select=i;
				}
		 else
		 if(Algo==2)
			for(;i<N;i++)
				{if((P[i].arrival_time<=T)&&
				    (P[i].time_required>0)&&
				   ((P[i].time_required<P[select].time_required)||
				   ((P[i].time_required==P[select].time_required)&&
				    (P[i].arrival_time<P[select].arrival_time))))
					select=i;
				}
		 else
		 if(Algo==3)
			for(;i<N;i++)
				{if((P[i].arrival_time<=T)&&
				    (P[i].time_required>0)&&
				   ((P[i].priority<P[select].priority)||
				   ((P[i].priority==P[select].priority)&&
				    (P[i].arrival_time<P[select].arrival_time))))
					select=i;
				}
		 else
		 if(Algo==4)
			for(;i<N;i++)
				{if((P[i].arrival_time<=T)&&
				    (P[i].time_required>0)&&
				   ((P[i].waiting_since<P[select].waiting_since)||
				   ((P[i].waiting_since==P[select].waiting_since)&&
				    (P[i].arrival_time>P[select].arrival_time))))
					select=i;
				}
		 else
		 if(Algo==5)
			for(;i<N;i++)
				{if((P[i].arrival_time<=T)&&
				    (P[i].time_required>0)&&
				   ((P[i].queue_assigned<P[select].queue_assigned)||
				   ((P[i].queue_assigned==P[select].queue_assigned)&&
				    (P[i].waiting_since<P[select].waiting_since))||
				   ((P[i].queue_assigned==P[select].queue_assigned)&&
				    (P[i].waiting_since==P[select].waiting_since)&&
				    (QI[P[i].queue_assigned].algo==1)&&
				    (P[i].arrival_time<P[select].arrival_time))||
				   ((P[i].queue_assigned==P[select].queue_assigned)&&
				    (P[i].waiting_since==P[select].waiting_since)&&
				    (QI[P[i].queue_assigned].algo==2)&&
				    (P[i].arrival_time>P[select].arrival_time))))
					select=i;
				   }
		 else
		 if(Algo==6)
			for(;i<N;i++)
				{if((P[i].arrival_time<=T)&&
				    (P[i].time_required>0)&&
				   ((P[i].queue_assigned<P[select].queue_assigned)||
				   ((P[i].queue_assigned==P[select].queue_assigned)&&
				    (P[i].waiting_since<P[select].waiting_since))||
				   ((P[i].queue_assigned==P[select].queue_assigned)&&
				    (P[i].waiting_since==P[select].waiting_since)&&
				    (P[i].queue_assigned==NQ-1)&&
				    (P[i].arrival_time<P[select].arrival_time))||
				   ((P[i].queue_assigned==P[select].queue_assigned)&&
				    (P[i].waiting_since==P[select].waiting_since)&&
				    (P[i].queue_assigned<NQ-1)&&
				    (P[i].arrival_time>P[select].arrival_time))))
					select=i;
				}
		 RUNNING=select;
		 P[RUNNING].waiting_time+=(T-P[RUNNING].waiting_since);
		 if(Algo==4)
			TQ_left=TQ-1;
		 // Starting
		 if(P[RUNNING].response_time==-1)
			{if(((Algo==5)&&(QI[P[RUNNING].queue_assigned].algo==2))||(Algo==6))
				P[RUNNING].tq_left=QI[P[RUNNING].queue_assigned].tq-1;
			 P[RUNNING].response_time=T-P[RUNNING].arrival_time;
			 cout<<T<<" ms: "<<P[RUNNING].name<<" started.\n";
			}
		 // Resumption
		 else
			{P[RUNNING].tq_left--;
			 cout<<T<<" ms: "<<P[RUNNING].name<<" resumed.\n";
			}
		}
	}
  // Running
  else
	{P[RUNNING].time_required--;
	 if(Algo==4)
		TQ_left--;
	 else
	 if((Algo==5)&&(QI[P[RUNNING].queue_assigned].algo==2))
		P[RUNNING].tq_left--;
	 else
	 if((Algo==6)&&(P[RUNNING].queue_assigned<NQ-1))
		P[RUNNING].tq_left--;
	 // Termination
	 if(P[RUNNING].time_required==0)
		{P[RUNNING].termination_time=T;
		 cout<<T<<" ms: "<<P[RUNNING].name<<" terminated.\n";
		 if(DL)
			{RUNNING=-2;
			 DL_left=DL;
			 Just_dl=1;
			}
		 else
			{RUNNING=-1;
			 Just_idle=1;
			}
		 T--;
		 // Termination
		 COMPLETE=1;
		 for(i=0;i<N;i++)
			if(P[i].time_required>0)
				{COMPLETE=0;
				 break;
				}
		}
	}
  T++;
 }


 // RESULTS *******************************************************************

 // getch();
 cout<<"Turnaround time -\n";
 sum=0;
 for(i=0;i<N;i++)
	{cout<<"\t"<<P[i].name<<": "<<P[i].termination_time-P[i].arrival_time<<" ms.\n";
	 sum+=P[i].termination_time-P[i].arrival_time;
	}
 mean=sum*1.0/N;
 sd=0;
 for(i=0;i<N;i++)
	sd+=(P[i].termination_time-P[i].arrival_time-mean)*(P[i].termination_time-P[i].arrival_time-mean);
 sd=sqrt(sd/N);
 cout<<"\tMean: "<<mean<<" ms, sd: "<<sd<<" ms.\n";

 cout<<"Waiting time -\n";
 sum=0;
 for(i=0;i<N;i++)
	{cout<<"\t"<<P[i].name<<": "<<P[i].waiting_time<<" ms.\n";
	 sum+=P[i].waiting_time;
	}
 mean=sum*1.0/N;
 sd=0;
 for(i=0;i<N;i++)
	sd+=(P[i].waiting_time-mean)*(P[i].waiting_time-mean);
 sd=sqrt(sd/N);
 cout<<"\tMean: "<<mean<<" ms, sd: "<<sd<<" ms.\n";

 cout<<"Response time -\n";
 sum=0;
 for(i=0;i<N;i++)
	{cout<<"\t"<<P[i].name<<": "<<P[i].response_time<<" ms.\n";
	 sum+=P[i].response_time;
	}
 mean=sum*1.0/N;
 sd=0;
 for(i=0;i<N;i++)
	sd+=(P[i].response_time-mean)*(P[i].response_time-mean);
 sd=sqrt(sd/N);
 cout<<"\tMean: "<<mean<<" ms, sd: "<<sd<<" ms.\n";

 cout<<"Throughput: "<<N*1.0/T<<" process/ms.\n";

 sum=0;
 for(i=0;i<N;i++)
	sum+=P[i].cpu_burst_time;
 cout<<"CPU utilization: "<<100-(T-sum)*100.0/T<<"%.\n";

 // getch();
}