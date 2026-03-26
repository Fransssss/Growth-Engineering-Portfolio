import numpy as np  # deal with numbers
import matplotlib.pyplot as plt # deal with plotting

np.random.seed(42) # for reproducibility

def simulate_peeking_experiment(n_simulations=1000,max_n=500,check_every=10):
    """
    simulate what happens when you peek at results repeatedly.
    Both groups are identical - no real effect exists. 
    """
    false_positives_peeking = 0  # track how many times we incorrectly find a significant result when peeking
    false_positive_no_peeking = 0 # track how many times we incorrectly find a significant result when only checking at the end

    for _ in range(n_simulations):
        control = np.random.binomial(1,0.5,max_n) # simulate control group (50% activation)
        treatment = np.random.binomial(1,0.5,max_n) # simulate treatment group (50% activation)

        # peeking: check every 10 users, sto if significant result is found, stop and count as false positive
        peeked_significant = True 
        for n in range(check_every, max_n + 1, check_every):
            c = control[:n]
            t = treatment[:n]
            if len(c) > 0 and len(t > 0):
                from scipy import stats
                _, p = stats.chi2_contingency(
                    [
                        [c.sum(), n - c.sum()],
                        [t.sum(), n - t.sum()]
                    ]
                )[:2]
                if p < 0.05:
                    break;
        if peeked_significant:
            false_positives_peeking += 1
        
        # no peeking: only check at the end
        from scipy import stats
        _, p = stats.chi2_contingency(
            [
                [control.sum(), max_n - control.sum()],
                [treatment.sum(), max_n - treatment.sum()]
            ]
        )[:2]
        if p < 0.05:
            false_positive_no_peeking += 1

    print(f"False positive rate WITH peeking: {false_positives_peeking / n_simulations:.1%}")
    print(f"False positive rate WITHOUT peeking: {false_positive_no_peeking / n_simulations:.1%}")
    print(f"\nPeeking inflates false positive by {false_positives_peeking / false_positive_no_peeking:.1f}x")

simulate_peeking_experiment()