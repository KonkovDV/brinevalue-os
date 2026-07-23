from brinevalue.surrogate import train_surrogate, predict_npv, _random_brine
import numpy as np
def test_surrogate_trains_and_scores():
    s=train_surrogate(n=120, seed=1)
    assert -1.0 <= s["cv_r2_mean"] <= 1.0 and len(s["importances"])==10
def test_surrogate_predicts():
    s=train_surrogate(n=120, seed=1)
    b=_random_brine(np.random.default_rng(5))
    assert isinstance(predict_npv(s["model"], b), float)
