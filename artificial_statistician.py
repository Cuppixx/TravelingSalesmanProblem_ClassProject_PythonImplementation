from itertools import combinations
import math
import matplotlib.pyplot as plt
from scipy.stats import shapiro, anderson, kstest, ttest_ind, mannwhitneyu, ks_2samp, rankdata
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
    print("Let's compare", len(sequences),"sequences at an alpha-level of", alpha,"\n")
    print("*****************************************")
    print("Let's first have a look at the properties of the data distributions:\n")
    
    normality_results = {}
    for name, seq in sequences.items():
        print (name)
        print ("sequence: ", seq)

        # normality tests
        # Shapiro-Wilk
        a_shapiro = shapiro(seq)
        print("{:30s} {:30f}".format("Shapiro-Wilk: p-value", a_shapiro[1]))

        # Kolmogorov-Smirnov
        a_kolmogorov = kstest(seq, 'norm')
        print("{:30s} {:30f}".format("Kolmogorov-Smirnov: p-value", a_kolmogorov[1]))

        # Anderson
        a_anderson = anderson(seq, dist='norm')
        print("{:30s} {:30f}".format("Anderson: test statistic", a_anderson[0]))
        print("{:30s} {:30f}".format("Anderson: critical value", a_anderson[1][2]),"\n")

        normality_results[name] = (a_shapiro[1] > alpha, a_kolmogorov[1] > alpha, a_anderson[0] < a_anderson[1][2])

        # plot histogram
        plot_histogram(seq, name)
        
    print("*****************************************")
    print ("Let's continue with comparing the", len(sequences), "sequences:")

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
                print("{:30s} {:30f}".format("t-statistic", ttest_ab[0]))
                print("{:30s} {:30f}".format("p-value", ttest_ab[1]))
            else:
                print("\nT-test assuming norm. distr. & unequal sigmas")
                ttest_ab_unequal = ttest_ind(seq_a, seq_b, equal_var=False)
                print("{:30s} {:30f}".format("t-statistic", ttest_ab_unequal[0]))
                print("{:30s} {:30f}".format("p-value", ttest_ab_unequal[1]))
        else:
            print("\nAt least one distribution is not normal")
            print("\nMann - Whitney U test/ Wilcoxon rank-sum test")
            mannwhitney = mannwhitneyu(seq_a, seq_b, alternative="two-sided")
            print("{:30s} {:30f}".format("p-value", mannwhitney[1]))

        print("\nKolmogorov Smirnov(a,b) test")
        kolmog = ks_2samp(seq_a, seq_b)  # Compute the Kolmogorov-Smirnov statistic on 2 samples.
        print("{:30s} {:30f}".format("p-value", kolmog[1]))

        # effect measures
        c = list(seq_a) + list(seq_b)
        c_ranked = rankdata(c, method='average')
        a_ranked = list(c_ranked[:len(seq_a)])
        b_ranked = list(c_ranked[len(seq_a):len(seq_a) + len(seq_b)])
        ranksum_a = sum(a_ranked)
        ranksum_b = sum(b_ranked)

        print("\nVargha’s and Delaney’s A Measure")
        print("0.5=no, 0.56=small, 0.64=medium, 0.71=big effect")
        A = 1 / len(seq_b) * (ranksum_a / len(seq_a) - (len(seq_a) + 1) / 2)
        if A < 0.5:
            A = 1 - A
        print("{:30s} {:30f}".format("A measure", A))

        print("\nCohens d measure")
        print("0.25=small, 0.5=medium 0.75=large effect")
        s_pooled = math.sqrt((variance(seq_a) + variance(seq_b)) / 2)
        d = (mean(seq_a) - mean(seq_b)) / s_pooled
        print("{:30s} {:30f}".format("d measure", d))

        # Hedges g measure (p.344 lecture 2018)
        hedges_g2 = (mean(seq_a) - mean(seq_b)) / (
                    ((len(seq_a) - 1) * math.sqrt(variance(seq_a)) ** 2 + (len(seq_b) - 1) * math.sqrt(variance(seq_b)) ** 2) / ((len(seq_a) + len(seq_b) - 2))) ** 0.5
        print("{:30s} {:31f}".format("\nhedges g", hedges_g2))
        hedges_g1 = d * (1 - (3 / (4 * (len(seq_a) + len(seq_b)) - 9)))
        print("{:30s} {:30f}".format("hedges g (Korrekturfaktor)", hedges_g1))

        # Glass delta measure
        print("\nGlass delta measure")
        if len(seq_a) > len(seq_b):
            glass_delta = (mean(seq_b) - mean(seq_a)) / math.sqrt(variance(seq_a))
            print("{:30s} {:30f}".format("\nGlass delta measure", glass_delta))

        if len(seq_b) > len(seq_a):
            glass_delta = (mean(seq_a) - mean(seq_b)) / math.sqrt(variance(seq_b))
            print("{:30s} {:30f}".format("\nGlass delta measure", glass_delta))

        if len(seq_a) == len(seq_b):
            glass_delta1 = (mean(seq_a) - mean(seq_b)) / math.sqrt(variance(seq_b))
            glass_delta2 = (mean(seq_b) - mean(seq_a)) / math.sqrt(variance(seq_a))
            print("{:30s} {:30f}".format("Calculate with Std.Dev(a)", glass_delta2))
            print("{:30s} {:30f}".format("Calculate with Std.Dev(b)", glass_delta1))


test_all(sequences, alpha)