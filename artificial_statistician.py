# pylint: skip-file
from itertools import combinations
import math
import matplotlib.pyplot as plt # type: ignore
from scipy.stats import shapiro, anderson, kstest, ttest_ind, mannwhitneyu, ks_2samp, rankdata # type: ignore
from statistics import variance, mean

# Sequences
a = [0.0300, 0.9100, 0.6400, 0.9900, 0.6400, 0.1600, 0.1600, 0.9100, 0.1600, 0.2700]
b = [0.6400, 0.0800, 0.1600, 0.2700, 0.0200, 0.0100, 0.1600, 0.0300, 0.0300, 0.6400]
c = [0.3300, 0.2900, 0.1700, 0.4700, 0.4800, 0.2600, 0.1800, 0.2300, 0.3100, 0.2100]

# Sort data
a_sorted = list(sorted(a))
b_sorted = list(sorted(b))
c_sorted = list(sorted(c))

# Names of sequences
name_a = "Algorithm 1"
name_b = "Algorithm 2"
name_c = "Algorithm 3"

# Set alpha level
alpha = 0.05

# Create dict
sequences = {name_a:a_sorted, name_b:b_sorted, name_c:c_sorted}


def plot_histogram(data, title):
    plt.hist(data, bins='auto', alpha=0.7, rwidth=0.85)
    plt.title(f'Histogram of {title}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()


def plot_boxplot(data1, data2, title1, title2):
    data = [data1, data2]
    plt.boxplot(data, patch_artist=True, labels=[title1, title2])
    plt.title('Box plot comparison')
    plt.ylabel('Value')
    plt.show()


def test_all(sequences, alpha):
    print("This is an Artificial Statistician for continuous target values and unpaired data!")
    print(f"Let's compare {len(sequences)} sequences at an alpha-level of {alpha} \n")
    print("*****************************************")
    print("Let's first have a look at the properties of the data distributions:\n")

    normality_results = {}
    for name, seq in sequences.items():
        print(name)
        print(f"sequence: {seq}")

        # normality tests
        # Shapiro-Wilk
        a_shapiro = shapiro(seq)
        print(f"{'Shapiro-Wilk: p-value':30s} {a_shapiro[1]:30f}")

        # Kolmogorov-Smirnov
        a_kolmogorov = kstest(seq, 'norm')
        print(f"{'Kolmogorov-Smirnov: p-value':30s} {a_kolmogorov[1]:30f}")

        # Anderson
        a_anderson = anderson(seq, dist='norm')
        print(f"{'Anderson: test statistic':30s} {a_anderson[0]:30f}")
        print(f"{'Anderson: critical value':30s} {a_anderson[1][2]:30f}\n")

        normality_results[name] = (a_shapiro[1] > alpha, a_kolmogorov[1] > alpha, a_anderson[0] < a_anderson[1][2])

        # plot histogram
        plot_histogram(seq, name)

    print("*****************************************")
    print(f"Let's continue with comparing the {len(sequences)} sequences:")

    for (name_a, seq_a), (name_b, seq_b) in combinations(sequences.items(), 2):
        print(f"\nComparing {name_a} and {name_b}:")

        # plot box plot
        plot_boxplot(seq_a, seq_b, name_a, name_b)

        # Check normality
        a_normal = all(normality_results[name_a])
        b_normal = all(normality_results[name_b])

        if a_normal and b_normal:
            print("\nBoth distributions are normal")
            # Check variances
            var_a = variance(seq_a)
            var_b = variance(seq_b)

            if abs(var_a - var_b) / max(var_a, var_b) < 0.1:
                print("\nT-test assuming norm. distr. & equal sigmas")
                ttest_ab = ttest_ind(seq_a, seq_b)
                print(f"{'t-statistic':30s} {ttest_ab[0]:30f}"); print(f"{'p-value':30s} {ttest_ab[1]:30f}")

            else:
                print("\nT-test assuming norm. distr. & unequal sigmas")
                ttest_ab_unequal = ttest_ind(seq_a, seq_b, equal_var=False)
                print(f"{'t-statistic':30s} {ttest_ab_unequal[0]:30f}"); print(f"{'p-value':30s} {ttest_ab_unequal[1]:30f}")

        else:
            print("\nAt least one distribution is not normal\nMann - Whitney U test/ Wilcoxon rank-sum test")
            mannwhitney = mannwhitneyu(seq_a, seq_b, alternative="two-sided")
            print(f"{'p-value':30s} {mannwhitney[1]:30f}")

        print("\nKolmogorov Smirnov(a,b) test")
        kolmog = ks_2samp(seq_a, seq_b)  # Compute the Kolmogorov-Smirnov statistic on 2 samples.
        print(f"{'p-value':30s} {kolmog[1]:30f}")

        # effect measures
        c = list(seq_a) + list(seq_b)
        c_ranked = rankdata(c, method='average')
        a_ranked = list(c_ranked[:len(seq_a)])
        b_ranked = list(c_ranked[len(seq_a):len(seq_a) + len(seq_b)])
        ranksum_a = sum(a_ranked)
        ranksum_b = sum(b_ranked)

        print("\nVarghas and Delaneys A Measure\n0.5=no, 0.71=big effect")
        A = 1 / len(seq_b) * (ranksum_a / len(seq_a) - (len(seq_a) + 1) / 2)
        if A < 0.5: A = 1 - A
        print(f"{'A measure':30s} {A:30f}")

        print("\nCohens d measure\n0.25=small, 0.5=medium, 0.75=large effect")
        s_pooled = math.sqrt((variance(seq_a) + variance(seq_b)) / 2)
        d = (mean(seq_a) - mean(seq_b)) / s_pooled
        print(f"{'d measure':30s} {d:30f}")

        # Hedges g measure (p.344 lecture 2018)
        hedges_g2 = (mean(seq_a) - mean(seq_b)) / (((len(seq_a) - 1) * math.sqrt(variance(seq_a)) ** 2 + (len(seq_b) - 1) * math.sqrt(variance(seq_b)) ** 2) / ((len(seq_a) + len(seq_b) - 2))) ** 0.5
        print(f"{'hedges g':30s} {hedges_g2:31f}")
        
        hedges_g1 = d * (1 - (3 / (4 * (len(seq_a) + len(seq_b)) - 9)))
        print(f"{'hedges g (Korrekturfaktor)':30s} {hedges_g1:30f}")

        # Glass delta measure
        print("\nGlass delta measure")

        if len(seq_a) > len(seq_b):
            glass_delta = (mean(seq_b) - mean(seq_a)) / math.sqrt(variance(seq_a))
            print(f"{'Glass delta measure':30s} {glass_delta:30f}")

        if len(seq_b) > len(seq_a):
            glass_delta = (mean(seq_a) - mean(seq_b)) / math.sqrt(variance(seq_b))
            print(f"{'Glass delta measure':30s} {glass_delta:30f}")

        if len(seq_a) == len(seq_b):
            glass_delta1 = (mean(seq_a) - mean(seq_b)) / math.sqrt(variance(seq_b))
            glass_delta2 = (mean(seq_b) - mean(seq_a)) / math.sqrt(variance(seq_a))
            print(f"{'Calculate with Std.Dev(a)':30s} {glass_delta2:30f}")
            print(f"{'Calculate with Std.Dev(b)':30s} {glass_delta1:30f}")


test_all(sequences, alpha)
