
"""
read real HRM samples from a csv and use a wavelet transform with overlapping windows
to extract heart rate data
"""

# import numpy as np
from numpy import *
from math import pi
from random import sample, random
import matplotlib.pyplot as plt
from pylab import plot, show, title, xlabel, ylabel, subplot, xlim, ylim
from scipy import fft, arange
import csv
import sys

def mainLoop(sampleList):
	lastWindow = -1
	windowDiff = 64
	# windowLength = 20
	windowLength = 256
	windowCount = 0
	index = 0
	for sample in sampleList:
		time = sample[0]
		# if we're at the start of a window make an array to be processed
		# if lastWindow == -1 or time-lastWindow > windowDiff:
		if lastWindow == -1 or index-lastWindow > windowDiff:
			windowCount += 1
			# lastWindow = time
			lastWindow = index
			windowList = list()
			for sample in sampleList:
				# if sample[0] >= time and sample[0] < lastWindow + windowLength:
				if sample[0] >= time and len(windowList) < windowLength:
					windowList.append(sample)
			# if windowList[len(windowList)-1][0] - windowList[0][0] < windowLength - 1:
			if len(windowList) < windowLength:
				return
			windowTransform(windowList)
			return
			# print 'in window ' + str(lastWindow) + ' to ' + str(windowList[len(windowList)-1][0]) + ', heart rate: ' + str(60*windowTransform(windowList))
		index += 1

def windowTransform(windowList):
	n = len(windowList)			# samples
	samp_rate = 64 # getRate(windowList)	# Hz
	# print "rate: " + str(samp_rate)
	levels = 7
	wave = getWave(windowList)

	# Can't detect frequencies that could not oscillate >= 2 times in the window
	# low_cutoff = 1 / ((len(windowList)/samp_rate)/2)
	low_cutoff = 0
	high_cutoff = 8
	# print "low cutoff: " + str(low_cutoff)

	# cA, cD = dwt(wave, 'db2')
	coeffs = my_wavedec(wave, level=levels)

	i = 0
	# print len(coeffs)
	nyquist = samp_rate / 2.

	freqs = zeros(levels)
	freq_bounds = zeros(levels+1)
	freq_widths = zeros(levels)
	powers = zeros(levels)
	freq_range = nyquist - low_cutoff

	for a in coeffs:
		if (i <> 0):
			lower_limit = nyquist / 2.**(levels-i+1)
			upper_limit = nyquist / 2.**(levels-i)
			# print i, len(a), mean(abs(a)), std(a), lower_limit, upper_limit
			# I don't know why the 2 to 1 ratio works better...
			# freqs[i-1] = (2 * lower_limit + upper_limit) / 3.
			freqs[i-1] = (lower_limit + upper_limit) / 2.
			if(i == 1):
				freq_bounds[i-1] = lower_limit
			freq_bounds[i] = upper_limit
			# freqs[i-1] = (lower_limit + 2 * upper_limit) / 3.

			# weight the frequencies by the widths of their bins
			# this could be a problem since the largest bin is 512 times the smallest
			# and later on the sum will always be skewed that way
			# freq_widths[i-1] = (upper_limit - lower_limit) / nyquist
			if ( i <> 1):
				freq_widths[i-1] = freqs[i-1] - freqs[i-2]
			if (freqs[i-1] < high_cutoff and freqs[i-1] > low_cutoff):
				powers[i-1] = mean(abs(a))
			else:
				powers[i-1] = 0
			# print "power " + str(powers[i-1])
			 # powers[i-1] = mean(abs(a)) if (freqs[i-1] <= 8.0 and freqs[i=1] >= .5) else 0	# ignore frequencies higher than 4 Hz
		i += 1

	core_freq = 0.
	numerator = 0.
	denominator = 0.

	# print str(freqs)

	for i in arange(levels):
		if (i <> 0 and (powers[i] + powers[i-1]) <> 0):
			Area = (freq_widths[i]/2)*(powers[i] + powers[i-1])
			numerator += ((freq_widths[i]**2)/6)*(2*powers[i] + powers[i-1]) * freq_widths[i]
			denominator += (freq_widths[i]/2)*(powers[i] + powers[i-1]) * freq_widths[i]
			
			# numerator += (1/freq_widths[i])*Area*(freq_widths[i]/2 + (freq_widths[i]/6)*((powers[i]-powers[i-1])/(powers[i]+powers[i-1])) + freqs[i-1])
			# denominator += (1/freq_widths[i])*Area
			
			# numerator += powers[i-1]*(freqs[1]**2 - freqs[i-1]**2)/2 + (powers[i]-powers[i-1])*(freqs[i]**3 - freqs[i]**3)/(3*freq_widths[i])
			
			# numerator += (powers[i-1]/2)*(freq_bounds[i]**2-freq_bounds[i-1]**2)
			# denominator += (powers[i-1])*(freq_bounds[i]-freq_bounds[i-1])
			# print "N: " + str(numerator) + "   (h: " + str(freq_widths[i]) + ", b1: " + str(powers[i-1]) + ", b2: " + str(powers[i]) + "\nD: " + str(denominator)
	core_freq = numerator/denominator

	print 'in window ' + str(windowList[0][0]) + ' to ' + str(windowList[len(windowList)-1][0]) + ', heart rate: ' + str(60*core_freq)
	plt.plot(freqs,powers)
	plt.xlim(0, 10)
	plt.grid()
	plt.show()
	return core_freq	

def getRate(windowList):
	numSamples = len(windowList)
	timeElapsed = windowList[numSamples-1][0]-windowList[0][0]
	rate = numSamples/timeElapsed
	return rate

def getWave(windowList):
	wave = list()
	for sample in windowList:
		wave.append(sample[1])
	return wave

def getTime(windowList):
	time = list()
	for sample in windowList:
		time.append(sample[0])
	return time

def getFactor(n, i):
	# factor = (n+1)/2 + abs((n-1)/2 - i)
	factor = 1 + abs((n-1)/2 - i)
	scale = 1
	return 1/float(scale*factor)

def freqSkew(n, i):
	scale = .25
	if(i < (n-1)/2):
		factor = 1 + scale*abs((n-1)/2 - i)
	else:
		factor = 1 - scale*abs((n-1)/2 - i)
	return factor

def plotFFTSpectrum(y,Fs):
	"""
	Plots a Single-Sided Amplitude Spectrum of y(t)
	"""
	n = len(y) # length of the signal
	k = arange(n)
	T = n/Fs
	frq = k/T # two sides frequency range
	frq = frq[range(n/2)] # one side frequency range

	Y = fft(y)/n # fft computing and normalization
	Y = Y[range(n/2)]

	plot(frq,abs(Y),'r') # plotting the spectrum
	xlim(0, 4)
	# set_xticks(arange(0, 5, .25))
	xlabel('Freq (Hz)')
	ylabel('|Y(freq)|')


def readFile():
	sampleList = list()
	with open('samples_finger_02.csv','rU') as samplesFile:
		reader = csv.reader(samplesFile, dialect=csv.excel_tab)
		for row in reader:
			valuePair = row[0].split(",", 1)
			sampleList.append(map(float, valuePair))
	return sampleList

def waveGen():
	n = 4096			# samples
	freq0 = 0 	# Hz
	samp_rate = 64	# Hz
	levels = 8

	start_freq = 1	# Hz
	end_freq = 2	# Hz
	if (start_freq != end_freq):
		freq0 = arange(start_freq, end_freq, (end_freq - start_freq) / (n * 1.0))
	else:
		freq0 = start_freq


	factor0 = samp_rate / freq0
	time = arange(n)/float(samp_rate)
	wave0 = sin(2 * pi * freq0 * time)

	# errors = [random() - 0.5 for _ in range(n)]
	# wave0 += errors

	sampleList = list()
	for t in arange(len(time)):
		sample = [time[t], wave0[t]]
		sampleList.append(sample)

	return sampleList

def printTransformArray(sampleList):
	i = 0
	transformArray = []
	sys.stdout.write("{")
	for sample in sampleList:
		if (i <> 256 and i <> 0):
			sys.stdout.write(", ")
		sys.stdout.write(str(sample[1]))
		transformArray.append(sample[1])
		i += 1 
		if (i == 256):
			sys.stdout.write("}; \n {")
		if(i == 326):
			sys.stdout.write("};")
			return transformArray


def my_wavedec(data, level=None):
	coeffs_list = []
	length = len(data) >> 1
	a = array(zeros(length), float) #list(zeros(length))
	d = array(zeros(length), float) #list(zeros(length))
	for j in xrange(level):
		a = array(zeros(length), float) #list(zeros(length))
		d = array(zeros(length), float) #list(zeros(length))
		for i in xrange(length):
			total = data[i*2] + data[i*2+1]
			diff = data[i*2] - data[i*2+1]
			a[i] = total
			d[i] = diff

		data = a
		coeffs_list.append(d)

		# print "length = " + str(length) + " a: " + str(a) + ", d: " + str(d)
		length = length >> 1
	coeffs_list.append(a)
	coeffs_list.reverse()
	return coeffs_list

def rawData():
	# sampleList = list();
	sampleList = [[0.01, 777], [0.03, 777], [0.05, 775], [0.06, 763], [0.08, 734], [0.09, 694], [0.11, 645], [0.12, 591], [0.14, 539], [0.15, 511], [0.17, 448], [0.19, 415], [0.20, 393], [0.22, 379], [0.23, 374], [0.25, 373], [0.26, 374], [0.28, 378], [0.29, 385], [0.31, 393], [0.33, 403], [0.34, 416], [0.36, 429], [0.37, 441], [0.39, 452], [0.40, 460], [0.42, 466], [0.44, 471], [0.45, 474], [0.47, 478], [0.48, 481], [0.50, 485], [0.51, 490], [0.53, 495], [0.55, 503], [0.56, 509], [0.58, 516], [0.59, 524], [0.61, 534], [0.62, 542], [0.64, 550], [0.65, 558], [0.67, 565], [0.69, 571], [0.70, 577], [0.72, 584], [0.73, 591], [0.75, 679], [0.76, 614], [0.78, 617], [0.80, 621], [0.81, 626], [0.83, 696], [0.84, 642], [0.86, 644], [0.87, 647], [0.89, 651], [0.90, 654], [0.92, 656], [0.94, 658], [0.95, 661], [0.97, 662], [0.98, 714], [1.00, 638], [1.01, 607], [1.03, 570], [1.04, 528], [1.06, 486], [1.08, 447], [1.09, 413], [1.11, 387], [1.12, 449], [1.14, 355], [1.15, 349], [1.17, 349], [1.19, 352], [1.20, 360], [1.22, 373], [1.23, 390], [1.25, 408], [1.26, 425], [1.28, 440], [1.29, 451], [1.31, 457], [1.33, 458], [1.34, 453], [1.36, 444], [1.37, 434], [1.39, 427], [1.40, 422], [1.42, 421], [1.44, 421], [1.45, 423], [1.47, 426], [1.48, 431], [1.50, 471], [1.51, 451], [1.53, 454], [1.54, 459], [1.56, 465], [1.58, 471], [1.59, 477], [1.61, 482], [1.62, 486], [1.64, 490], [1.65, 494], [1.67, 498], [1.69, 501], [1.70, 505], [1.72, 509], [1.73, 514], [1.75, 520], [1.76, 526], [1.78, 533], [1.79, 539], [1.81, 545], [1.83, 656], [1.84, 602], [1.86, 533], [1.87, 508], [1.89, 476], [1.90, 438], [1.92, 399], [1.94, 455], [1.95, 392], [1.97, 305], [1.98, 287], [2.00, 278], [2.01, 276], [2.03, 278], [2.04, 283], [2.06, 294], [2.08, 309], [2.09, 327], [2.11, 347], [2.12, 366], [2.14, 383], [2.15, 397], [2.17, 454], [2.19, 416], [2.20, 415], [2.22, 412], [2.23, 408], [2.25, 405], [2.26, 405], [2.28, 407], [2.29, 412], [2.31, 420], [2.33, 431], [2.34, 445], [2.36, 461], [2.37, 477], [2.39, 494], [2.40, 510], [2.42, 525], [2.44, 540], [2.45, 555], [2.47, 568], [2.48, 580], [2.50, 589], [2.51, 596], [2.53, 601], [2.54, 604], [2.56, 607], [2.58, 608], [2.59, 609], [2.61, 609], [2.62, 610], [2.64, 612], [2.65, 614], [2.67, 617], [2.69, 621], [2.70, 626], [2.72, 632], [2.73, 637], [2.75, 637], [2.76, 617], [2.78, 576], [2.79, 519], [2.81, 454], [2.83, 390], [2.84, 333], [2.86, 287], [2.87, 252], [2.89, 230], [2.90, 220], [2.92, 219], [2.94, 222], [2.95, 229], [2.97, 240], [2.98, 255], [3.00, 272], [3.01, 291], [3.03, 401], [3.04, 352], [3.06, 360], [3.08, 372], [3.09, 383], [3.11, 394], [3.12, 403], [3.14, 410], [3.15, 415], [3.17, 419], [3.19, 422], [3.20, 426], [3.22, 431], [3.23, 437], [3.25, 445], [3.26, 453], [3.28, 482], [3.29, 482], [3.31, 487], [3.33, 494], [3.34, 503], [3.36, 512], [3.37, 521], [3.39, 529], [3.40, 535], [3.42, 540], [3.44, 545], [3.45, 548], [3.47, 550], [3.48, 552], [3.50, 553], [3.51, 553], [3.53, 660], [3.54, 607], [3.56, 556], [3.58, 558], [3.59, 561], [3.61, 566], [3.62, 572], [3.64, 579], [3.65, 585], [3.67, 586], [3.69, 566], [3.70, 527], [3.72, 477], [3.73, 421], [3.75, 366], [3.76, 318], [3.78, 280], [3.79, 250], [3.81, 232], [3.83, 222], [3.84, 221], [3.86, 223], [3.87, 228], [3.89, 236], [3.90, 248], [3.92, 263], [3.94, 278], [3.95, 295], [3.97, 309], [3.98, 320], [4.00, 328], [4.01, 332], [4.03, 333], [4.04, 331], [4.06, 329], [4.07, 329], [4.09, 330], [4.11, 333], [4.12, 338], [4.14, 346], [4.15, 355], [4.17, 365], [4.19, 377], [4.20, 389], [4.22, 402], [4.23, 415], [4.25, 427], [4.26, 439], [4.28, 450], [4.29, 460], [4.31, 468], [4.32, 475], [4.34, 482], [4.36, 487], [4.37, 490], [4.39, 492], [4.40, 494], [4.42, 497], [4.43, 500], [4.45, 503], [4.47, 507], [4.48, 512], [4.50, 518], [4.51, 524], [4.53, 530], [4.54, 648], [4.56, 589], [4.57, 506], [4.59, 467], [4.61, 416], [4.62, 358], [4.64, 301], [4.65, 248], [4.67, 203], [4.68, 169], [4.70, 145], [4.72, 129], [4.73, 122], [4.75, 119], [4.76, 120], [4.78, 123], [4.79, 128], [4.81, 136], [4.82, 145], [4.84, 156], [4.86, 169], [4.87, 181], [4.89, 194], [4.90, 204], [4.92, 213], [4.93, 220], [4.95, 225], [4.97, 229], [4.98, 232], [5.00, 236], [5.01, 241], [5.03, 247], [5.04, 255], [5.06, 264], [5.07, 275], [5.09, 286], [5.11, 298], [5.12, 311], [5.14, 324], [5.15, 337], [5.17, 349], [5.18, 361], [5.20, 372], [5.22, 382], [5.23, 391], [5.25, 400], [5.26, 409], [5.28, 417], [5.29, 424], [5.31, 431], [5.32, 437], [5.34, 443], [5.36, 450], [5.37, 456], [5.39, 463], [5.40, 469], [5.42, 474], [5.43, 479], [5.45, 484], [5.47, 489], [5.48, 489], [5.50, 473], [5.51, 442], [5.53, 400], [5.54, 352], [5.56, 300], [5.57, 249], [5.59, 205], [5.61, 169], [5.62, 143], [5.64, 127], [5.65, 119], [5.67, 119], [5.68, 121], [5.70, 127], [5.71, 137], [5.73, 150], [5.75, 167], [5.76, 185], [5.78, 203], [5.79, 221], [5.81, 237], [5.82, 252], [5.84, 263], [5.86, 272], [5.87, 280], [5.89, 287], [5.90, 294], [5.92, 301], [5.93, 309], [5.95, 318], [5.96, 329], [5.98, 341], [6.00, 355], [6.01, 370], [6.03, 385], [6.04, 400], [6.06, 416], [6.07, 430], [6.09, 443]]
	while len(sampleList) > 256:
		sampleList.pop()
	return sampleList

if __name__ == '__main__':
	# sampleList = readFile()
	# sampleList = waveGen()
	sampleList = rawData();
	mainLoop(sampleList)
	# printTransformArray(sampleList)
	plt.plot(getTime(sampleList), getWave(sampleList))
	plt.show()
	# plt.plot(printTransformArray(sampleList))
	# plt.show()
