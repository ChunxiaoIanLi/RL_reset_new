#include "backtrack.h"
#include "decide.h"
#include "internal.h"
#include "limits.h"
#include "logging.h"
#include "print.h"
#include "reluctant.h"
#include "report.h"
#include "restart.h"

#include <inttypes.h>
#include <math.h>
#include <time.h>
#include "Thompson.hpp"

bool
kissat_restarting (kissat * solver)
{
  assert (solver->unassigned);
  if (!GET_OPTION (restart))
    return false;
  if (!solver->level)
    return false;
  if (CONFLICTS < solver->limits.restart.conflicts)
    return false;
  kissat_switch_search_mode (solver);
  if (solver->stable)
    return kissat_reluctant_triggered (&solver->reluctant);
  const double fast = AVERAGE (fast_glue);
  const double slow = AVERAGE (slow_glue);
  const double margin = (100.0 + GET_OPTION (restartmargin)) / 100.0;
  const double limit = margin * slow;
  LOG ("restart glue limit %g = %.02f * %g (slow glue) %c %g (fast glue)",
       limit, margin, slow,
       (limit > fast ? '>' : limit == fast ? '=' : '<'), fast);
  return limit <= fast;
}

void
kissat_new_focused_restart_limit (kissat * solver)
{
  assert (!solver->stable);
  limits *limits = &solver->limits;
  uint64_t delta = GET_OPTION (restartint) - 1;
  delta += kissat_logn (solver->statistics.restarts);
  limits->restart.conflicts = CONFLICTS + delta;
  kissat_extremely_verbose (solver, "next focused restart scheduled at %"
			    PRIu64 " after %" PRIu64 " conflicts",
			    limits->restart.conflicts, delta);
}

static unsigned
reuse_stable_trail (kissat * solver)
{
  const unsigned next_idx = kissat_next_decision_variable (solver);
  const heap *scores = solver->heuristic==0?&solver->scores:&solver->scores_chb;
  const unsigned next_idx_score = kissat_get_heap_score (scores, next_idx);
  LOG ("next decision variable score %u", next_idx_score);
  unsigned res = 0;
  while (res < solver->level)
    {
      frame *frame = &FRAME (res + 1);
      const unsigned decision_idx = IDX (frame->decision);
      const double decision_idx_score =
	kissat_get_heap_score (scores, decision_idx);
      LOG ("decision variable %u at level %u score %g",
	   decision_idx, res + 1, decision_idx_score);
      if (next_idx_score > decision_idx_score)
	break;
      res++;
    }
  return res;
}

static unsigned
reuse_focused_trail (kissat * solver)
{
  const unsigned next_idx = kissat_next_decision_variable (solver);
  const links *links = solver->links;
  const unsigned next_idx_stamp = links[next_idx].stamp;
  LOG ("next decision variable stamp %u", next_idx_stamp);
  unsigned res = 0;
  while (res < solver->level)
    {
      frame *frame = &FRAME (res + 1);
      const unsigned decision_idx = IDX (frame->decision);
      const unsigned decision_idx_stamp = links[decision_idx].stamp;
      LOG ("decision variable %u at level %u stamp %u",
	   decision_idx, res + 1, decision_idx_stamp);
      if (next_idx_stamp > decision_idx_stamp)
	break;
      res++;
    }
  return res;
}

static unsigned
reuse_trail (kissat * solver)
{
  unsigned res;
  if (solver->stable)
    res = reuse_stable_trail (solver);
  else
    res = reuse_focused_trail (solver);
  if (res)
    {
      INC (restarts_reused_trails);
      ADD (reused_levels, res);
      LOG ("restart reuses trail at decision level %u", res);
    }
  else
    LOG ("restarts does not reuse the trail");
  return res;
}

void restart_mab(kissat * solver){   
	unsigned stable_restarts = 0;
	solver->mab_reward[solver->heuristic] += !solver->mab_chosen_tot?0:log2(solver->mab_decisions)/solver->mab_chosen_tot;
	for (all_variables (idx)) solver->mab_chosen[idx]=0;
	solver->mab_chosen_tot = 0;
	solver->mab_decisions = 0;
	for(unsigned i=0;i<solver->mab_heuristics;i++) stable_restarts +=  solver->mab_select[i];
	if(stable_restarts < solver->mab_heuristics) {
		solver->heuristic = solver->heuristic==0?1:0; 
	}else{
		double ucb[2];
		solver->heuristic = 0;
		for(unsigned i=0;i<solver->mab_heuristics;i++) {
		     ucb[i] = solver->mab_reward[i]/solver->mab_select[i] + sqrt(solver->mabc*log(stable_restarts+1)/solver->mab_select[i]);
		     if(i!=0 && ucb[i]>ucb[solver->heuristic]) solver->heuristic = i;
		  }
	}
	solver->mab_select[solver->heuristic]++; 
}

void
kissat_restart (kissat * solver)
{
  START (restart);  
  INC (restarts);
  
  unsigned old_heuristic = solver->heuristic;
  if (solver->stable && solver->mab) 
     restart_mab(solver);
  unsigned new_heuristic = solver->heuristic;

  unsigned level = old_heuristic==new_heuristic?reuse_trail (solver):0;

  kissat_extremely_verbose (solver,
			    "restarting after %" PRIu64 " conflicts"
			    " (scheduled at %" PRIu64 ")",
			    CONFLICTS, solver->limits.restart.conflicts);
  LOG ("restarting to level %u", level);

  if (solver->stable && solver->mab) solver->heuristic = old_heuristic;
  kissat_backtrack (solver, level);
  if (solver->stable && solver->mab) solver->heuristic = new_heuristic;

  // RESET:
  // Do reset here
  // If DECISION_LEVEL == 0, full restart
  // DO_RESET(), based on the learning rate...
  // Rebuild_Heap()
  //  -> If heap.isEmpty == false
  //  ->    Pop()
  //  ->

  // printf("level: %d\n", level);   
  if(level != 0){
    //printf("decisions: %d\n", solver->reset_decisions);
    //printf("conflicts: %d\n", solver->reset_conflicts);
    // Seed the random number generator
    srand(time(NULL));

    //Thompson

    //compute local learning rate
    double localLearningRate = (solver->reset_conflicts * 1.0) / solver->reset_decisions;
    solver-> reset_conflicts = 0;
    solver-> reset_decisions = 0;
    //printf("local learning rate: %0.2f\n", localLearningRate);
    //printf("learning rateEMB: %0.2f\n\n", solver->learningRateEMA);
    //update success and failures
    if (solver-> resetTotalTimes != 0){
      if (localLearningRate >= solver->learningRateEMA){
        	if (solver->resetPrevLever == 0){
        	  solver->reset_wins++;
        	}
        	else{
        	  solver->restart_wins++;
        	}
      }
      else{
      	if (solver->resetPrevLever == 0){
      	  solver->reset_loses++;
      	}
      	else{
      	  solver->restart_loses++;
      	}
      }
    }
    //update LLR-MAB
    solver-> learningRateEMA *= solver-> resetDecay;
    solver->learningRateEMA += localLearningRate * (1.0 - solver->resetDecay);

    // printf("reset_wins: %0.2f\n", solver->reset_wins);
    // printf("reset_loses: %0.2f\n", solver->reset_loses);
    // printf("restart_wins: %0.2f\n", solver->restart_wins);
    // printf("restart_loses: %0.2f\n", solver->restart_loses);
    //select a lever
    solver->resetPrevLever = select_lever(solver->reset_wins, solver->reset_loses, solver->restart_wins, solver->restart_loses);
    solver->resetTotalTimes++;
    if (solver->resetPrevLever == 0){
      solver->reset_wins *= solver->resetDecay;
      solver->reset_loses *= solver->resetDecay;
    }
    else{
      solver->restart_wins *= solver->resetDecay;
      solver->restart_loses *= solver->resetDecay;
    }

    //printf("lever: %d\n\n",solver->resetPrevLever);

    // Probability of the event occurring (e.g. 0.3 means 30% chance)
    //double probability = 0.5;
    // Generate a random number between 0 and 1
    //double random_number = (double) rand() / RAND_MAX;
    // Check if the event occurs
    //if (random_number <= probability) {
    if (solver->resetPrevLever == 0) {
      // Event occurred, execute the code here
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
    kissat_new_focused_restart_limit (solver);

  if (solver->stable && solver->mab && old_heuristic!=new_heuristic) kissat_update_scores(solver);

  REPORT (1, 'R');
  STOP (restart); 
}
