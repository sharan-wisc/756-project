/* Copyright (c) ACM/SIGDA
	 Prepared by Geert Janssen, geert@us.ibm.com
	 */

/* ------------------------------------------------------------------------ */
/* INCLUDES								    */
/* ------------------------------------------------------------------------ */

#include <math.h>
#include "parser.h"
#include <time.h>
#include <stdint.h>
#include <stdlib.h>

uint64_t diff; 
struct timespec start, end;     //for calculating the time
#define BILLION 1000000000L


/* ------------------------------------------------------------------------ */
/* LOCAL DEFINES                                                            */
/* ------------------------------------------------------------------------ */

/* Define this to resort to a simple-minded solution approach. */
#define _CHICKEN

/* Accuracy in comparing two floating point numbers for equality. */
#define EPS		1e-5
#define EQUAL(a,b)	(fabs((a) - (b)) < EPS)

#define min(a,b)	((a) < (b) ? (a) : (b))
#define max(a,b)	((a) > (b) ? (a) : (b))

#define OFLAG(x)	((x)->flag)
#define OPAIR(x)	((x)->p)
#define OTIME(x)	PTIME(OPAIR(x))
#define OLOAD(x)	PLOAD(OPAIR(x))
#define ONEXT(x)	((x)->next)

#define PTIME(x)	((x).T)
#define PLOAD(x)	((x).L)

#define VISIT_MASK	0x1
#define VISIT(x)	(FLAG(x) |  VISIT_FLAG)
#define UNVISIT(x)	(FLAG(x) & ~VISIT_FLAG)
#define VISITED(x)	(!!(FLAG(x) & VISIT_FLAG))

#define OPTS_GET(x)	((Options) T_DATA(x))
#define OPTS_SET(x,o)	(T_DATA(x) = (x))

/* ------------------------------------------------------------------------ */
/* LOCAL TYPE DEFINITIONS                                                   */
/* ------------------------------------------------------------------------ */

typedef unsigned int	Bool;
typedef unsigned int	Nat;
typedef double		Time;
typedef double		Capacitance;
typedef double		Resistance;
typedef double		Length;

/* An option pair. */
typedef struct Pair_S {
	Time T;			/* required arrival time */
	Capacitance L;		/* overall capacitive load */
} Pair;

/* A list of option pairs. */
typedef struct Options_S *Options;
struct Options_S {
	/*Nat flag;*/			/* as yet unused */
	Pair p;			/* the element pair */
	Options next;			/* rest of list or NULL */
};

/* ------------------------------------------------------------------------ */
/* VARIABLES		                                                    */
/* ------------------------------------------------------------------------ */
/* ADDED FOR ECE756 HWK */
/* Boolean variable added to add a bunch of debug messages for merge/filter */
static Bool my_debug = 0;
/* END ADDED FOR ECE756 HWK */

static Bool debug = 0;

/* Per unit wire length resistance and capacitance values: */
static Resistance	R_unit =  0.1; /* [Ohm/m] */
static Capacitance	C_unit =  0.2; /* [F/m] */
//static Resistance	R_unit =  0.003; /* [Ohm/m] */ //r1 benchmark
//static Capacitance	C_unit = 0.02; /* [F/m] */ //r1 benchmark

/* Buffer parameters: */
static Resistance	R_buf  = 10.0; /* Ohm */
static Capacitance	C_buf  =  4.0; /* femto Farad */
//static Resistance	R_buf  = 5.0; /* Ohm *///Sizing up by twice
//static Capacitance	C_buf  =  8.0; /* femto Farad *///Sizing up by twice
static Time		D_buf  =  2.0; /* nano sec */

/* ------------------------------------------------------------------------ */
/* FUNCTION DEFINITIONS                                                     */
/* ------------------------------------------------------------------------ */

/* Returns the pair (T,L). */
	static Pair
pair_mk(Time T, Capacitance L)
{
	Pair p;

	PTIME(p) = T;
	PLOAD(p) = L;
	return p;
}

	static void
pair_show(FILE *fp, Pair p)
{
	fprintf(fp, "(%.2f, %.2f)", PTIME(p), PLOAD(p));
}

	static Options
option_mk(Pair p)
{
	Options o = malloc(sizeof(*o));

	OPAIR(o) = p;
	ONEXT(o) = NULL;
	return o;
}

	static void
option_free(Options o)
{
	if (o)
		free(o);
}

#if 0
	static Options
options_copy(Options o)
{
	Options Z, *tail = &Z;

	while (o) {
		*tail = option_mk(OPAIR(o));
		tail = &ONEXT(*tail);
		o = ONEXT(o);
	}
	return Z;
}
#endif
	static Nat
options_len(Options o)
{
	Nat len;

	for (len = 0; o; o = ONEXT(o), len++)
		;
	return len;
}
//#endif

	static Options
options_last(Options o)
{
	while (o) {
		Options next = ONEXT(o);

		if (!next)

			return o;
		o = next;
	}
	return NULL;
}

	static void
options_free(Options o)
{
	while (o) {
		Options next = ONEXT(o);
		option_free(o);
		o = next;
	}
}

	static void
options_show(FILE *fp, Options o, const char *msg)
{
	fprintf(fp, "%s", msg);
	while (o) {
		Options next;

		pair_show(fp, OPAIR(o));
		next = ONEXT(o);
		if (next)
			fprintf(fp, ", ");
		o = next;
	}
	fprintf(fp, "\n");
}

	static void
node_options_show(FILE *fp, Options o, Tree k)
{
	char buf[64];

	sprintf(buf, "%s: ", T_NAME(k));
	options_show(stdout, o, buf);
}

/* ------------------------------------------------------------------------ */

/* Returns (singleton) options list for sink node k. */
	static Options
options_sink(Tree k)
{
	Options Z;

	Z = option_mk(pair_mk(T_TIME(k), T_LOAD(k)));
	if (debug)
		options_show(stdout, Z, "Sink:\n");
	return Z;
}


/************************************************/
/* (FILLED BY YOU) */

/* Filter out inferior pairs from the Options list.*/
static Options options_filter(Options Z, Nat len){

	Options o, prev_o, temp;
	Time rat = -1.797693e+308;	//Setting RAT to the least possible value
	Capacitance load = 1.797693e+308;	//Setting Load to the highest possible value
	prev_o = Z; // To keep track of previous node

	//Iterating over the entire list
	for (o = Z ; o;){ 

		//Look for Max RAT
		if (rat < OTIME(o)){ 
			rat = OTIME(o);
			load = OLOAD(o);
		}

		//If RATs are same, select least capacitance
		else if ((rat == OTIME(o)) && (load > OLOAD(o))){
			load = OLOAD(o);
		}

		//Check if the node is inferior and remove from the list, update the pointer accordingly
		if(rat > OTIME(o) && load < OLOAD(o)){
			temp = o;
			ONEXT(prev_o) = ONEXT(o);
			o = ONEXT(o);
			free(temp);
		}
		else{
			prev_o = o;
			o = ONEXT(o);
		}
	}

	//Append the best node at the end of the existing list
	OTIME(options_last(Z)) = rat;
	OLOAD(options_last(Z)) = load;
	ONEXT(options_last(Z)) = NULL;
	return Z;
}

/************************************************/

/* Add wire segment of length l.
	 Update rules:

	 T = T - R * C / 2.0 - R * L
	 L = L + C

	 Returns possibly modified options list Z.
	 */
	static Options
options_add_wire(Options Z, Length l)
{
	Resistance  R = R_unit * l;
	Capacitance C = C_unit * l;
	Options o;
	Nat len;

	for (o = Z, len = 0; o; o = ONEXT(o), len++) {
		OTIME(o) -= R * (C / 2.0 + OLOAD(o));
		OLOAD(o) += C;
	}
	if (debug)
		options_show(stdout, Z, "Added wire:\n");

	return options_filter(Z, len);
}

/* Add buffer option.
	 Update rules:

	 T = T - Dbuf - Rbuf * L
	 L = Cbuf

	 Returns possibly modified options list Z.
	 */
	static Options
options_add_buffer(Options Z)
{
	Options *tail, o;
	Nat len;
	Time Tmax;

#ifdef CHICKEN
	/* For each option, calculate new option when buffer is added, and
		 insert that new option right after the original one.
		 Of course this disrupts the order and also might introduce redundant
		 options, therefore must explicitly sort/filter the list.
		 */
	for (o = Z, len = 0; o; o = ONEXT(o), len++) {
		Time    T = OTIME(o) - D_buf - R_buf * OLOAD(o);
		Options n = option_mk(pair_mk(T, C_buf));

		/* Insert n after o: */
		ONEXT(n) = ONEXT(o);
		ONEXT(o) = n;
		o = n;
		len++;
	}
	if (debug)
		options_show(stdout, Z, "Added buffer:\n");

	Z = options_filter(Z, len);
#else
	/* Determine Tmax: */

	/* Get reference time by adding buffer to first option element: */
	o = Z;
	Tmax = OTIME(o) - D_buf - R_buf * OLOAD(o);
	/* Compare against rest of elements if any: */
	o = ONEXT(o);
	len = 1;
	while (o) {
		/* Get effect of adding buffer to this option element: */
		Time T = OTIME(o) - D_buf - R_buf * OLOAD(o);

		if (T > Tmax)
			Tmax = T;
		o = ONEXT(o);
		len++;
	}
	/* Note: Tmax <= OTIME(o) for some o elem Z. */

	/* Find location to (possibly) insert buffer option (Tmax,C_buf): */
	tail = &Z;
	o = *tail;
	while (OTIME(o) < Tmax) {
		tail = &ONEXT(o);
		o = *tail;
	}
	/* Here: must have Tmax <= OTIME(o) */

	if (EQUAL(OTIME(o), Tmax)) {
		/* Prune the existing option or the buffer option: */
		if (C_buf < OLOAD(o))
			/* This element o becomes the buffer option: */
			OLOAD(o) = C_buf;
		/* else discard buffer option. */
	}
	else { /* Here: Tmax < OTIME(o) */
		if (C_buf < OLOAD(o)) {
			/* Insert buffer option before element o: */
			*tail = option_mk(pair_mk(Tmax, C_buf));
			ONEXT(*tail) = o;
		}
		/* else discard buffer option. */
	}
	if (debug)
		options_show(stdout, Z, "Added buffer:\n");
#endif
	return Z;
}



/* (FILLED BY YOU) */
	inline static Options
options_merge(Options o1, Options o2)
{
	/*Find merged capacitive loading and RAT of the combined solution
		Note you can make use of the function option_mk here to allocate new solution*/
	Time T;
	Capacitance L;
	/*
		 if (OTIME(o1) < OTIME(o2))
		 T = OTIME(o1);
		 else
		 T = OTIME(o2);
		 */
	if (my_debug) {
		options_show(stderr, o1, "options_merge o1:");  
		options_show(stderr, o2, "options_merge o2:");  
	}

	T = min(OTIME(o1), OTIME(o2));
	L = OLOAD(o1) + OLOAD(o2);

	if(my_debug) fprintf(stderr, "options_merge output: (%2f, %2f)\n\n", T, L);

	return option_mk(pair_mk(T, L));
} 

/*
	 Cartesian product of option sets with on-the-fly pruning.
	 Update rules:

	 T = min(T1, T2)
	 L = L1 + L2

	 Returns freshly created options list Z.
	 */
	static Options
options_combine(Options Z1, Options Z2)
{
	Options Z, o1, o2;
	
	Options *tail;
	Nat len=0;
  Nat len_z1 = options_len(Z1);
	Nat len_z2 = options_len(Z2);
	Z1 = options_filter(Z1, len_z1);
	Z2 = options_filter(Z2, len_z2);
//	quickSort(Z1);
//	quickSort(Z2);
	/* Combine every option element from Z1 with every option element from
		 Z2. The merge operation is symmetric so this approach is sufficient
		 to generate all possible combinations. The merge results are stored
		 in a new list Z.
		 Of course this list need not be ordered and very likely contains
		 redundant options, therefore must explicitly sort/filter the list.
		 */

	tail=&Z;

Nat iterator;
Capacitance load = 1.797693e+308; //Setting Load to the highest possible value
Time rat = -1.797693e+308;  //Setting RAT to the least possible value
Options n;
//printf("Entering merging\n");
	for (o1=Z1; o1; o1 = ONEXT(o1)){
		iterator = 0;
		for (o2=Z2; o2; o2 = ONEXT(o2)) {
			iterator++;
			if (OTIME(o2) >= OTIME(o1)) {
				if (OLOAD(o2) < load) {
					load = OLOAD(o2);
					rat = OTIME(o2);
				}
			}
			if (iterator == len_z2) {
				if (rat != -1.797693e+308) {
					n = option_mk(pair_mk(rat, load));
					*tail = options_merge(o1, n); 
					tail=&ONEXT(*tail);
					len ++;
				}
			}
		}
	}


load = 1.797693e+308; //Setting Load to the highest possible value
rat = -1.797693e+308;  //Setting RAT to the least possible value
	for (o2=Z2; o2; o2 = ONEXT(o2)){
		iterator = 0;
		for (o1=Z1; o1; o1 = ONEXT(o1)) {
			iterator++;
			if (OTIME(o1) >= OTIME(o2)) {
				if (OLOAD(o1) < load) {
					load = OLOAD(o1);
					rat = OTIME(o1);
				}
			}
			if (iterator == len_z1) {
				if (rat != -1.797693e+308) {
					n = option_mk(pair_mk(rat, load));
					*tail = options_merge(o2, n); 
					tail=&ONEXT(*tail);
						len ++;
				}
			}
		}
	}


	if (debug) options_show(stdout, Z, "test");
//	len = options_len(tail);
	Z = options_filter(Z, len); 

	/* Delete original lists: */
	options_free(Z1);
	options_free(Z2);
	return Z;
}
/************************************************/

/* It is assumed that option lists are < sorted w.r.t. both time and load
	 values. For any two elements (a1,b1) and (a2,b2) in the list we have
	 that if (a1,b1) appears before (a2,b2) then a1 < a2 and b1 < b2.
	 */

/* Lukas P.P.P. van Ginneken algorithm for optimal buffer insertion in
	 RC-tree.
	 */
	Options
options_sort(Options list)
{
	Options o1, o2;
	Time rat;	
	Capacitance load;	
	//	printf("Inside sort\n");
	int count = 0;
	o1 = list;
	//Iterating over the entire list
	for (o1 = list ; o1; o1 = ONEXT(o1)){ 
		for (o2 = ONEXT(o1); o2; o2 = ONEXT(o2)){
			//			printf("Check time %f\n", OTIME(o2));
			if(OTIME(o2) > OTIME(o1)){
				rat = OTIME(o2);
				load = OLOAD(o2);
				/*				printf("BEfore parsing\n");
									printf("Check time o2 %f\n", OTIME(o2));
									printf("Check load o2 %f\n", OLOAD(o2));
									printf("Check time o1 %f\n", OTIME(o1));
									printf("Check load o1 %f\n", OLOAD(o1));
									*/				OTIME(o2) = OTIME(o1);
				OLOAD(o2) = OLOAD(o1);
				OTIME(o1) = rat;
				OLOAD(o1) = load;
				/*				printf("After parsing\n");
									printf("Check time o2 %f\n", OTIME(o2));
									printf("Check load o2 %f\n", OLOAD(o2));
									printf("Check time o1 %f\n", OTIME(o1));
									printf("Check load o1 %f\n", OLOAD(o1));
									count ++;
									*///				printf("Count value is \t %d\n", count);
			}
		}
	}

	return list;

}


// Partitions the list taking the last element as the pivot
Options partition(Options head, Options end,
		Options *newHead, Options *newEnd)
{
	Options pivot = end;
	Options prev = NULL, cur = head, tail = pivot;

	// During partition, both the head and end of the list might change
	// which is updated in the newHead and newEnd variables
	while (cur != pivot)
	{
		if (OTIME(cur) < OTIME(pivot))
		{
			// First node that has a value less than the pivot - becomes
			// the new head
			if ((*newHead) == NULL)
				(*newHead) = cur;

			prev = cur;  
			cur = ONEXT(cur);
		}
		else // If cur node is greater than pivot
		{
			// Move cur node to next of tail, and change tail
			if (prev)
				ONEXT(prev) = ONEXT(cur);
			Options tmp = ONEXT(cur);
			ONEXT(cur) = NULL;
			ONEXT(tail) = cur;
			tail = cur;
			cur = tmp;
		}
	}

	// If the pivot data is the smallest element in the current list,
	// pivot becomes the head
	if ((*newHead) == NULL)
		(*newHead) = pivot;

	// Update newEnd to the current last node
	(*newEnd) = tail;

	// Return the pivot node
	return pivot;
}


//here the sorting happens exclusive of the end node
Options quickSortRecur(Options head)
{
	Options end = options_last(head);
	// base condition
	if (!head || head == end)
		return head;

	Options newHead = NULL, newEnd = NULL;

	// Partition the list, newHead and newEnd will be updated
	// by the partition function
	Options pivot = partition(head, end, &newHead, &newEnd);

	// If pivot is the smallest element - no need to recur for
	// the left part.
	if (newHead != pivot)
	{
		// Set the node before the pivot node as NULL
		Options tmp = newHead;
		while (ONEXT(tmp) != pivot)
			tmp = ONEXT(tmp);
		ONEXT(tmp) = NULL;

		// Recur for the list before pivot
		newHead = quickSortRecur(newHead);

		// Change next of last node of the left half to pivot
		tmp = options_last(newHead);
		ONEXT(tmp) =  pivot;
	}

	// Recur for the list after the pivot element
	ONEXT(pivot) = quickSortRecur(ONEXT(pivot));

	return newHead;
}

// The main function for quick sort. This is a wrapper over recursive
// function quickSortRecur()
void quickSort(Options list)
{
	list = quickSortRecur(list);
	return;
}



	static Options
bottom_up(Tree k, Bool no_buf)
{
	Options Z, Z1, Z2, o1, o2;

	if (T_LEAF(k))
		Z = options_sink(k);
	else {
		Z1 = bottom_up(T_SUB1(k), no_buf);
		Z2 = bottom_up(T_SUB2(k), no_buf);

		Z  = options_combine(Z1, Z2);

		/***************************/
	}
	Z = options_add_wire(Z, T_WIRE(k));
	if (!no_buf)
		Z = options_add_buffer(Z);
	if (debug)
		node_options_show(stdout, Z, k);
	return Z;
}

	int
main(int argc, char *argv[])
{
	Tree t;

clock_gettime(CLOCK_MONOTONIC, &start); //start time //
	if (argc > 1 && argv[1])
		if (!freopen(argv[1], "r", stdin)) {
			fprintf(stderr, "Cannot open file `%s' for reading.\n", argv[1]);
			return EXIT_FAILURE;
		}

	t = parse();

	pair_show(stdout, OPAIR(bottom_up(t, 1)));
	fprintf(stdout, "\n");
	pair_show(stdout, OPAIR(options_last(bottom_up(t, 0))));
	fprintf(stdout, "\n");
clock_gettime(CLOCK_MONOTONIC, &end); // end time //
diff = BILLION * (end.tv_sec - start.tv_sec) + end.tv_nsec - start.tv_nsec;

printf("elapsed process CPU time = %llu nanoseconds\n", (long long unsigned int) diff);
printf("elapsed process CPU time = %llu milliseconds\n", (long long unsigned int) (diff/1000000)); 

	return EXIT_SUCCESS;
}
