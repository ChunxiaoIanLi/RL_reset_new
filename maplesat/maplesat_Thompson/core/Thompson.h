#include <algorithm>
#include <iostream>
#include <iomanip>
#include <iterator>
#include <vector>
#include <boost/random.hpp>
#include <boost/random/discrete_distribution.hpp>
#include <boost/random/mersenne_twister.hpp>

// Define base_generator as a Mersenne Twister. This is needed only to make the
// code a bit less verbose.
typedef boost::mt19937 base_generator;

// argmax returns the index of maximum element in vector v.
template<class T>
size_t argmax(const std::vector<T>& v){
  return std::distance(v.begin(), std::max_element(v.begin(), v.end()));
}

// Thompson Variables
//
typedef struct Thompson_variable {
    // gen is a Mersenne Twister random generator. We initialzie it here to keep
    // the binary deterministic.
    base_generator gen;

    // Number of trials per bandit
    std::vector<double> trials;
    // Number of wins per bandif
    std::vector<double> wins;
    // Beta distributions of the priors for each bandit
    std::vector<boost::random::beta_distribution<> > prior_dists;

    Thompson_variable (int num_arms){
        trials = std::vector<double>(num_arms, 0);
        wins = std::vector<double>(num_arms, 0);
        // Initialize the prior distributions with alpha=1 beta=1
        for (size_t i = 0; i < num_arms; i++) {
            prior_dists.push_back(boost::random::beta_distribution<>(1, 1));
        }
    }

    unsigned int select_lever (){
        std::vector<double> priors;
        // Sample a random value from each prior distribution.
        for (auto& dist : prior_dists) {
            priors.push_back(dist(gen));
        }
        
        // Select the bandit that has the highest sampled value from the prior
        return static_cast<unsigned int>(argmax(priors));
    }

    void update_dist (unsigned int bandit_to_update, bool isWin) {
        

        trials[bandit_to_update]++;
        // trials[bandit_to_update^1]++;
        // Pull the lever of the chosen bandit
        
        // wins[bandit_to_update^1] += (isWin^1);
        
        // if (bandit_to_update == 0){
        //     wins[bandit_to_update] += isWin * 0.8;
        // } else {
        //     wins[bandit_to_update] += isWin;
        // }

        wins[0] *= 0.80;
        wins[1] *= 0.80;
        trials[0] *= 0.80;
        trials[1] *= 0.80;
        
        wins[bandit_to_update] += isWin;

        // Update the prior distribution of the chosen bandit
        
        auto alpha = 1 + wins[bandit_to_update];
        auto beta = 1 + (trials[bandit_to_update] - wins[bandit_to_update]);
     
        

        printf("No Reset wins/loss: (%.2f, %.2f)\n", wins[0], trials[0] - wins[0]);
        printf("   Reset wins/loss: (%.2f, %.2f)\n", wins[1], trials[1] - wins[1]);
        printf("No Reset Lever a/b: (%d, %d)\n", prior_dists[0].alpha(), prior_dists[0].beta());
        printf("   Reset Lever a/b: (%d, %d)\n", prior_dists[1].alpha(), prior_dists[1].beta());
        printf("a/b: (%d, %d)\n", alpha, beta);
        prior_dists[bandit_to_update] = boost::random::beta_distribution<>(alpha, beta);
    }

} Thompson_var;


