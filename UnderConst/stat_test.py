#############################
# ### Work with qc_full : fields_ratio 
########### 
 
import seaborn as sns
import scipy.stats as stats
import numpy as np
import random
import warnings
import matplotlib.pyplot as plt
import random
from random import sample


############################################

from scipy.stats import norm
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')

fig, ax = plt.subplot(1, 1)

mean, var, skew, kurt = norm.stats(moments='mvsk')

x  = np.linspace(norm.ppf(0.01),
                norm.ppf(0.99), 100)
ax.plot(x, norm.pdf(x),
       'r-', lw=5, alpha=0.6, label='norm pdf')

###########################################
#        
sns.set(rc={'figure.figsize':(13, 7.5)})
sns.set_context('talk')

# warnings.filterwarnings('ignore')
# plotfields = [plt.plot(fields_ratio[x]) for x in range(len(fields_ratio)) ]


# fig, ax = plt.subplot()
# warnings.warn(message, mplDeprecation, stacklevel=1)
fig, ax = plt.subplots(nrows=5, ncols=5)
ax = ax.flatten()

for row in ax:
    for col in row:
        col.plot()


for row in ax:
    for col in row:
        


fig1 =plt.figure(figsize=(5, 5), facecolor='w', edgecolor='k')

fig2 = subplot(5, 5, ii)


plotfields = []
for i in range(len(my_features_data[0])):
    newplt = [plt.hist(fields_ratio[i][x], bins=30, normed=True) for x in range(len(fields_ratio[i]))]
    plotfields.append(newplt)
    plt.title(str.format('Features\' ratios of sample {} by Fields', my_features_data[0][i][1]))
    ax[i] = newplt
    plt.savefig(mydir)

plt.show()

fig, plotfields = plt.subplots(nrows=5, ncols=5)
for row in plotfields:
    for col in row:
        col.hist()

    
str.format('{}.png',my_features_data[0][0][1]))               # fig.savefig('path/to/save/image/to.png')

    fields_ratio[0] # np.random.normal(loc=0, scale=10, size=6000)


hist = plt.hist(fields_ratio[0][0], bins=30, normed=True)

hist = plt.hist(values, bins=30, normed=True)
hist = plt.hist(values, bins=30, density=True)
hist = plt.hist(values, bins=30, density=True, cumulative=True)
hist = plt.hist2d(values, 30)

two_std_from_mean = np.mean(values) + np.std(values)*1.645
# Using Kernel Density estimation to estimate the PDF of a random variable. Non-parametric. Uni \ Multi Variate
kde = stats.gaussian_kde(values)
pos = np.linspace(np.min(values), np.max(values), 10000)
plt.plot(pos, kde(pos), color='teal')

shade = np.linspace(two_std_from_mean, 40, 300)
plt.fill_between(shade, kde(shade), alpha=0.45, color='teal')
plt.title("Sampling Distribution for One-Tail Hypothesis Test", y=1.015, fontsize=20)
plt.xlabel("sample mean value", labelpad=14)
plt.ylabel("frequency of occurence", labelpad=14)

#############################################
# Two-Tailed Hypothesis Tests

values = fields_ratio[0]                                                #np.random.normal(loc=0, scale=10, size=6000)
alpha_05_positive = np.mean(values) + np.std(values)*2.33               # choose z-score range for Positive tail
alpha_05_negative = np.mean(values) - np.std(values)*2.33               # choose z-score range for Negative tail
kde = stats.gaussian_kde(values)
pos = np.linspace(np.min(values), np.max(values), 10000)
plt.plot(pos, kde(pos), color='dodgerblue')
shade = np.linspace(alpha_05_positive, 40, 300)
plt.fill_between(shade, kde(shade), alpha=0.45, color='dodgerblue')
shade2 = np.linspace(alpha_05_negative, -40, 300)
plt.fill_between(shade2, kde(shade2), alpha=0.45, color='dodgerblue')
plt.title("Sampling Distribution for Two-Tail Hypothesis Test", y=1.015, fontsize=20)
plt.xlabel("sample mean value", labelpad=14)
plt.ylabel("frequency of occurence", labelpad=14);
plt.show()

########################


population_mean_pounds = sc.stats.tmean(fields_ratio[0])
population_size = len(fields_ratio[0])
population_std_dev_ratios = sc.stats.tstd(fields_ratio[0])

# np.random.seed(50)
# population_Ratios = np.random.normal(loc=population_mean_pounds, scale=population_std_dev_pounds, size=5500)

newlist = sample(fields_ratio[0],int(len(fields_ratio[0])/4))


treatment_sample_mean_pounds = sc.stats.tmean(ratio_means)

n = 30
ratio_means = []

for sample in range(0, 500):
    sample_values = np.random.choice(a=newlist, size=n)    
    sample_mean = np.mean(sample_values)
    ratio_means.append(sample_mean)

sns.distplot(ratio_means, color='darkviolet')
plt.title("Sampling Distribution ($n=30$) of Features' Ratios", y=1.015, fontsize=20)
plt.xlabel("sample mean ratio", labelpad=14)
plt.ylabel("frequency of occurence", labelpad=14);
plt.show()

standard_error_ratios = population_std_dev_ratios / np.sqrt(n)
standard_error_ratios

z_score = (treatment_sample_mean_pounds - population_mean_pounds)/standard_error_ratios
z_score