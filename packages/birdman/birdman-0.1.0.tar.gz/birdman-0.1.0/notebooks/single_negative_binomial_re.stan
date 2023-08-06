data {
  int<lower=1> N;                                   // number of sample IDs
  int<lower=1> num_subjs;                           // number of groups (subjects)
  int<lower=1> p;                                   // number of covariates
  real A;                                           // mean of intercept prior
  vector[N] log_depths;                             // sequencing depths of microbes
  matrix[N, p] x;                                   // covariate matrix
  array[N] int<lower=0, upper=num_subjs> subj_map;  // mapping of samples to subject IDs
  array[N] int y;                                   // observed microbe abundances
  real<lower=0> B_p;                                // stdev for covariate beta normal prior
  real<lower=0> inv_disp_sd;                        // stdev for inverse dispersion lognormal prior
  real<lower=0> re_p;                               // stdev for subject intercept normal prior
}

parameters {
  real<offset=A, multiplier=2> beta_0;              // intercept parameter
  vector[p-1] beta_x;                               // parameters for covariates
  real<lower=0> inv_disp;                           // inverse dispersion parameter
  vector[num_subjs] subj_re;                        // subject intercepts
}

transformed parameters {
  vector[p] beta_var = append_row(beta_0, beta_x);
  vector[N] lam = x*beta_var + log_depths;

  for (n in 1:N) {
    // add subject intercepts
    lam[n] += subj_re[subj_map[n]];
  }
}

model {
  // Specify priors
  beta_0 ~ normal(A, 2);
  for (i in 1:p-1) {
    beta_x[i] ~ normal(0, B_p);
  }

  subj_re ~ normal(0, re_p);
  inv_disp ~ lognormal(0, inv_disp_sd);

  // Fit model
  y ~ neg_binomial_2_log(lam, inv(inv_disp));
}

generated quantities {
  vector[N] y_predict;  // posterior predictive model
  vector[N] log_lhood;  // Evaluate log-likelihood of samples from posterior

  for (n in 1:N) {
    y_predict[n] = neg_binomial_2_log_rng(lam[n], inv(inv_disp));
    log_lhood[n] = neg_binomial_2_log_lpmf(y[n] | lam[n], inv(inv_disp));
  }
}
