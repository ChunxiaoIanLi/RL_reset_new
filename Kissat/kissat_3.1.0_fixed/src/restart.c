#include "restart.h"
#include "backtrack.h"
#include "bump.h"
#include "decide.h"
#include "internal.h"
#include "kimits.h"
#include "logging.h"
#include "print.h"
#include "reluctant.h"
#include "report.h"

#include <inttypes.h>
#include <math.h>
#include <time.h>
#include "Thompson.hpp"

bool kissat_restarting (kissat *solver) {
  assert (solver->unassigned);
  if (!GET_OPTION (restart))
    return false;
  if (!solver->level)
    return false;
  if (CONFLICTS < solver->limits.restart.conflicts)
    return false;
  if (solver->stable)
    return kissat_reluctant_triggered (&solver->reluctant);
  const double fast = AVERAGE (fast_glue);
  const double slow = AVERAGE (slow_glue);
  const double margin = (100.0 + GET_OPTION (restartmargin)) / 100.0;
  const double limit = margin * slow;
  kissat_extremely_verbose (solver,
                            "restart glue limit %g = "
                            "%.02f * %g (slow glue) %c %g (fast glue)",
                            limit, margin, slow,
                            (limit > fast    ? '>'
                             : limit == fast ? '='
                                             : '<'),
                            fast);
  return (limit <= fast);
}

void kissat_update_focused_restart_limit (kissat *solver) {
  assert (!solver->stable);
  limits *limits = &solver->limits;
  uint64_t restarts = solver->statistics.restarts;
  uint64_t delta = GET_OPTION (restartint);
  if (restarts)
    delta += kissat_logn (restarts) - 1;
  limits->restart.conflicts = CONFLICTS + delta;
  kissat_extremely_verbose (solver,
                            "focused restart limit at %" PRIu64
                            " after %" PRIu64 " conflicts ",
                            limits->restart.conflicts, delta);
}

void kissat_restart (kissat *solver) {
  START (restart);
  INC (restarts);
  if (solver->stable)
    INC (stable_restarts);
  else
    INC (focused_restarts);
  unsigned level = 0;
  kissat_extremely_verbose (solver,
                            "restarting after %" PRIu64 " conflicts"
                            " (limit %" PRIu64 ")",
                            CONFLICTS, solver->limits.restart.conflicts);
  LOG ("restarting to level %u", level);
  kissat_backtrack_in_consistent_state (solver, level);

  if(level != 0){
    srand(time(NULL));

    //Probability of the event occurring (e.g. 0.3 means 30% chance)
    double probability = 0.5;
    //Generate a random number between 0 and 1
    double random_number = (double) rand() / RAND_MAX;

    if (random_number < probability) {
      //reset activities
      for (all_variables(idx)) {
        kissat_update_heap(solver, &solver->scores, idx, (double) rand() / RAND_MAX*0.00001);
      }
      kissat_update_scores(solver);
      solver->nof_resets++;
    }
    else{
      solver->nof_restarts++; 
    }
  }
  else{
    solver->nof_restarts++;  
  }

  if (!solver->stable)
    kissat_update_focused_restart_limit (solver);


  REPORT (1, 'R');
  STOP (restart);
}
