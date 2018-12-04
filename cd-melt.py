import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from functions import *

parser = argparse.ArgumentParser()
parser.add_argument('-s', dest='startT', metavar="Starting temp", type=int, help="Enter starting temperature", required=True)
parser.add_argument('-f', dest='finalT', metavar="Final temp", type=int, help="Enter final temperature", required=True)
args = parser.parse_args()

startT = args.startT
finalT = args.finalT

#open csv file
infile = input('Name of CSV file: ')
title = input('Graph title: ')
peak = int(input('Which peak do you want to monitor? '))
data, names = opentext(infile, 2)
xp_name = infile.replace('.csv', '')

#plot multiline
plt.figure(1)
x = data[0]
y = data[1:]
plot_multiline(x, y, 'Wavelength [nm]', 'Ellipticity [mdeg]')
plt.axhline(0, color='black', linewidth="1") #add horiz line at y=0
plt.title(title)
filename = xp_name+'-CDMeltFull.png'
plt.savefig(filename, dpi=300)


#START NEXT PLOT
plt.figure(2)

elip = np.where(x == peak) #find which position in x = peak
#x_elip = x[elip] #find the value of x at the position calcd from above


plt.xlabel('Temperature [\u00b0C]')
plt.ylabel('Normalised Ellipiticity at '+str(peak)+' nm [mdeg]')

#set x values as every 5 between startT and finalT
newx = []
num = startT
while num <= finalT:
    newx.append(num)
    num += 5 #add 5 to startT and append it until you hit finalT, this is the x axis

#cut off last point in y, it errors for some reason, must be artifact of csv file
y = y[:-1]

#find each y at position of max y1 and make a new array of them
newy = [] #this will be the y axis
for i in y:
    newy.append(i[elip])

#normalised 0 to 1
normy = norm_zero_to_one(newy)

#fit curve
y_fit, melt = fit_curve(newx, normy)

#plot data
plot_fittedcurve(newx, normy, melt, y_fit)
plt.title(title)
filename = xp_name+'-CDMeltPeak.png'
plt.savefig(filename, dpi=300)
