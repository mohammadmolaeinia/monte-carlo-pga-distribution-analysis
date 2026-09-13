import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

#from pgaAnalysis.py we know number of PGAs : 12206.0000
#Mean or Average of PGAs : 34.3392
#Standard Deviation : 58.4308
#Range : 986.6504
#Skewness : 7.0695

#so becuse of skewness we use Lognormal Dist.
meanOfEx1 = 34.3392
stdOfEx1 = 58.4308

#make The parameters of Lognormal
logNormalSTD = np.sqrt(np.log(1 + (stdOfEx1 / meanOfEx1) ** 2))
logNormalMean = np.log(meanOfEx1) - 0.5*(logNormalSTD ** 2)

#now we go for Monte-Carlo

ranN = 1000000
rng = np.random.default_rng(seed=42)
lnpga = rng.lognormal(logNormalMean, logNormalSTD, ranN)
Y = (lnpga ** 2) - (2 * lnpga)

#for making Standard Deviation we need number of data and avrage of data
n = len(Y)
xAvrg = sum(Y) / n
stdD = math.sqrt((1 / (n - 1)) * sum((xi - xAvrg)**2 for xi in Y))

#for Range we need min and max X
xMin = min(Y)
xMax = max(Y)
Range = xMax - xMin

#for skewness we use Standard Devation that found in line 11
skewness = sum((xi - xAvrg)**3 for xi in Y) / (n * stdD**3)


#binning the data by Guessing The Bins Numers and Calclute Bins width, values and Centers
binsQty = 20
binsWidth = Range / binsQty
binsBorder = [xMin + i * binsWidth for i in range(binsQty + 1)]
binsCenters = [(binsBorder[i] + binsBorder[i+1]) / 2 for i in range(binsQty)]

#cunting the frequency of each bin by pga values one by one by for Loop
frequency = [0] * binsQty
for value in Y:
    for i in range(binsQty):
        #Assign frequencies to bins and handle the last bin to avoid dropping xMax
        if i == binsQty - 1:
            if binsBorder[i] <= value <= binsBorder[i+1]:
                frequency[i] += 1
                break
        else:
            if binsBorder[i] <= value < binsBorder[i+1]:
                frequency[i] += 1
                break

#finding the bin by highest frequency
maxFrequency = max(frequency)
maxBin = frequency.index(maxFrequency)
#for cdf we calclute the reletive frequency
relativeFrequency = [freq / n for freq in frequency]

#and now we do sum in each step and put the ans to the cdfValues
cdfValues = [0]
rltFreqSumStep = 0
for rf in relativeFrequency:
    rltFreqSumStep += rf
    cdfValues.append(rltFreqSumStep)

#finding the cdf and histogram widths
widths = [binsBorder[i+1] - binsBorder[i] for i in range(len(binsBorder)-1)]

#making figure of Histograme of PGA by frequency and prob of Observ
chartHist, ax1 = plt.subplots(figsize=(8, 5))
bars = ax1.bar(binsBorder[:-1], frequency, width=widths, align='edge', edgecolor='black', color='lightgray', linewidth=.5)
for bar in bars:
    height = bar.get_height()
    if height > 0: 
        ax1.text(bar.get_x() + bar.get_width()/2., height + (maxFrequency*0.03), f'{int(height)}', ha='center', va='top', fontsize=8, color='black')
ax1.xaxis.set_major_locator(ticker.FixedLocator(binsBorder))
ax1.set_xlabel('PGA (g)')
ax1.set_ylabel('Number of observations')
ax2 = ax1.twinx()
ax1_ylim = ax1.get_ylim()
ax2.set_ylim(ax1_ylim[0]/n , ax1_ylim[1]/n)
ax1.xaxis.set_tick_params(labelsize=6.5)
ax1.yaxis.set_tick_params(labelsize=6.5)
ax2.yaxis.set_tick_params(labelsize=6.5)
ax2.set_ylabel('Proportion of observations')
plt.title('1. Histogram of PGA (Frequency & Proportion)')
chartHist.tight_layout()

#making figure of CDF of PGA by cdfValues
chartCDF, ax3 = plt.subplots(figsize=(8, 5))
# Use plt.step for cumulative distributions
ax3.plot(binsBorder, cdfValues, color='red', linewidth=2, linestyle='-')
# Optional: Add points at the edges
ax3.plot(binsBorder, cdfValues, 'ro', markersize=3) 
ax3.set_xlabel('PGA (g)')
ax3.set_ylabel('Cumulative Probability F(x)')
ax3.set_ylim(0, 1.05)
ax3.xaxis.set_tick_params(labelsize=6.5)
ax3.yaxis.set_tick_params(labelsize=6.5)
plt.title('2.Cumulative Distribution Function (CDF)')
ax3.grid(True, linestyle='--', alpha=0.6)
chartCDF.tight_layout()

plt.show()
