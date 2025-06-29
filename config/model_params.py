from scipy.stats import randint, uniform

LIGHTGBM_PARAMS = {
    'n_estimators': randint(50, 150),
    'max_depth': randint(5, 50),
    'learning_rate': uniform(0.01, 0.1),
    'num_leaves': randint(16, 64),
    'boosting_type': ['gbdt', 'dart'],
    'force_col_wise': [True],
}

RANDOM_SEARCH_PARAMS = {
    'n_iter': 5,
    'cv': 5,
    'n_jobs': -1,
    'verbose': 2,
    'random_state': 42,
    'scoring': 'accuracy',
}