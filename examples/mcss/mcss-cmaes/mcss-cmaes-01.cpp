#include <mcss/McssCmaes.h>

#include <gsl/gsl_rng.h>

// variables for random weights
static gsl_rng *rng;
static double *random_weights;
static int weight_rounds = 100;
static double **target_data;
static double *timepoints;
static int num_timepoints;
static double *means;

// randomise random weights vector
void randomise_weights(void)
{
	int i;
	double sum;

	sum = 0.0;
	for(i = 0; i < targetDataRows(); i++) {
		random_weights[i] = gsl_rng_uniform_pos(rng);
		sum += random_weights[i];
	}
	for(i = 0; i < targetDataRows(); i++)
		random_weights[i] /= sum;
}

// initialise random number generator for random weights
extern "C" void initialise(void)
{
	rng = gsl_rng_alloc(gsl_rng_mt19937);
	gsl_rng_set(rng, cmaesParameters()->seed);

	if(!(random_weights = (double *) calloc(targetDataRows(), \
				sizeof(double)))) {
		fprintf(stderr, "error: unable to initialise random weights\n");
		exit(EXIT_FAILURE);
	}
	if(!(means = (double *) calloc(targetDataRows(), \
				sizeof(double)))) {
		fprintf(stderr, "error: unable to initialise means\n");
		exit(EXIT_FAILURE);
	}
	target_data = targetData();
	timepoints = targetDataTimepoints();
	num_timepoints = targetDataRows();
}

// set parameters of model
extern "C" void set_model_parameters(char *model_file, double *parameters, int run)
{
	sbml_set_parameter(model_file, "c1", pow(10.0, parameters[0]));
	sbml_set_parameter(model_file, "c2", pow(10.0, parameters[1]));
}

// calculate fitness over all runs
extern "C" double calculate_fitness(char **data_file)
{
	int i, j;
	double mean, error;

	mcss_average_level(data_file[0], "B", "c1::1:0,0", \
			timepoints, num_timepoints, means);
	mean = 0.0;
	for(i = 0; i < weight_rounds; i++) {
		// mean square error with random weights
		randomise_weights();
		error = 0.0;
		for(j = 0; j < num_timepoints; j++) {
			error += ((means[j] - target_data[j][1]) * \
					(means[j] - target_data[j][1]) * random_weights[j]);
		}
		mean += (error / (double) num_timepoints);
	}
	mean /= (double) weight_rounds;

	return mean;
}
