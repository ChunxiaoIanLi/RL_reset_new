#include <algorithm>
#include <iostream>
#include <iomanip>
#include <iterator>
#include <vector>
# include <cmath>
# include <limits>
// #include <boost/random.hpp>
// #include <boost/random/discrete_distribution.hpp>
// #include <boost/random/mersenne_twister.hpp>



// argmax returns the index of maximum element in vector v.
template<class T>
size_t argmax(const std::vector<T>& v){
  return std::distance(v.begin(), std::max_element(v.begin(), v.end()));
}

struct record {
    int bandit;
    double reward;
};

// UCB Variables
typedef struct UCB_variable {
    const int num_arms;
    std::vector<record> window;
    // double INITIAL_Q = 0.0;
    // const double ALPHA = 0.3;
    const double C = 0.2;
    const int window_sz = 30;

    UCB_variable (int num_arms): num_arms(num_arms)
    {
        // trials = std::vector<double>(num_arms, 0);
        // Qs = std::vector<double>(num_arms, INITIAL_Q);
    }

    unsigned int select_lever (){
        std::vector<double> Xs(num_arms, 0.0);
        std::vector<int> counts(num_arms, 0);
        for (size_t i = 0; i < window.size(); i++) {
            Xs[window[i].bandit] += window[i].reward;
            counts[window[i].bandit] ++;
        }
        std::vector<double> Qs(num_arms, 0.0);
        std::vector<double> EXPs(num_arms, 0.0);
        std::vector<double> UCBscores;
        // printf("\n");
        for (size_t i = 0; i < num_arms; i++) {
            if (counts[i] == 0) {
                Qs[i] = 0.0;
                EXPs[i] = std::numeric_limits<double>::infinity();
            } else {
                Qs[i] = Xs[i] / counts[i];
                EXPs[i] = C * sqrt(log(window.size())/counts[i]);
            }
            UCBscores.push_back(Qs[i] + EXPs[i]);
            // printf("Arm %d: Q: %f, EXP: %f(%d/%d), UCB: %f\n", i, Qs[i], EXPs[i], counts[i], window.size(), UCBscores[i]);
        }
        unsigned int max_index = static_cast<unsigned int>(argmax(UCBscores));
        // printf("Selected arm: %d\n", max_index);
        return static_cast<unsigned int>(argmax(UCBscores));
    }

    void update_qs (unsigned int bandit_to_update, double reward) {
        // printf("Updating bandit %d with local learning rate %f\n", bandit_to_update, reward);
        record r {bandit_to_update, reward};
        if (window.size() < window_sz) {
            window.push_back(r);
        } else {
            window.erase(window.begin());
            window.push_back(r);
        }
    }
} UCB_var;


