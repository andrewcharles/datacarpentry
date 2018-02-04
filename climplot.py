import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import calendar
from mpl_toolkits import basemap
import argparse

access_pr_file = "data/pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc"

def calc_prate_climo(filename=access_pr_file,month_name='Jan'):
    dset = xr.open_dataset(access_pr_file)
    prate = dset.variables['pr'] * 86400
    month_map = {}
    for i in range(1,12):
        month_map[calendar.month_abbr[i]] = i
    months = dset.groupby('time.month').groups
    month_idx = months[month_map[month_name]]
    month_prates = prate[month_idx,:,:]
    mean_prate = month_prates.mean(dim='time')
    lat,lon = dset.variables['lon'][:],dset.variables['lat'][:]
    return mean_prate,lat,lon


def plot_prate_climo(mean_prate,lat,lon,imgname='img.png'):
    plt.clf()
    bm = basemap.Basemap(llcrnrlon=0,llcrnrlat=-90, urcrnrlon=360, urcrnrlat=90)
    x,y = np.meshgrid(lat,lon)
    bm.contourf(x,y,mean_prate)
    bm.imshow(mean_prate)
    bm.drawcoastlines()
    plt.colorbar()

    parallels = np.arange(0.,81,10.)
    #labels = [left,right,top,bottom]
    bm.drawparallels(parallels,labels=[False,True,True,False])
    meridians = np.arange(10.,351.,20.)
    bm.drawmeridians(meridians,labels=[True,False,False,True])

    plt.savefig(imgname)


def main(argz):
    mean_prate,lat,lon = calc_prate_climo(filename=argz.infile,month_name=argz.month_name)
    plot_prate_climo(mean_prate,lat,lon,imgname=argz.outfile)


if __name__ == '__main__':
    description = "Plots climo things"
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("--infile", type=str, help="Input file name", 
        default=access_pr_file)
    
    parser.add_argument("--month_name", type=str, help="Name of month like Jan", 
        default='Jan', choices=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 
	'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    parser.add_argument("--outfile", type=str, default='img.png', help="Output file name")
    args = parser.parse_args()            
    main(args)


