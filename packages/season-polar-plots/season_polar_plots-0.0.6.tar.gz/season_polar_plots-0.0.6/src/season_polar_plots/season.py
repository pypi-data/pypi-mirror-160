# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:48:09 2022

@author: Marleen
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from scipy.stats import vonmises
from scipy.stats import t
from scipy.special import i0  
import math

class SeasonData:
    def __init__(self, data, start_year, end_year, t_res):
        if isinstance(data, pd.Series):
            data_ = pd.DataFrame(data)
            self.df = data_
        elif isinstance(data, pd.DataFrame):
            self.df = data
        else:
            raise TypeError('Input data must be pandas Series or DataFrame with DatetimeIndex')
        if not isinstance(self.df.index, pd.core.indexes.datetimes.DatetimeIndex):
            raise TypeError('DatetimeIndex for input data required')
        self.scaletime = pd.to_datetime('1704-01-01', format= '%Y-%m-%d')
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.start_year = int(start_year)
        self.end_year = int(end_year)
        self.years = list(range(self.start_year, self.end_year+1))
        self.t_res = t_res
    
   
    def t_theta(self, d):
        "radian scaling function for polar plots."
        return(d/366*(2 * np.pi))    
    

    def get_ev(self, mode, linreg=False, start_month = 1):
        """
        Function for daily time-series
        Arguments:
            mode: 'all' to select all data points, 'min' or 'max' to filter time series on annual extreme values
            linreg: default 'False', if 'True' calculates linear regression of days in year ~ years
            start_montht: default 1 (January), can be shifted for linear regression to any monthy of the year.
        Returns:
            Dataframe with days in year ('nday') of extreme values and filtered values ('value')
        """
        varname = self.df.columns[0]
        if not mode in ['all', 'max', 'min']:
            raise ValueError('"mode" must be "= all" or filter on extreme values: "= max" /"= min".')
        if mode =='all':
            df_ = self.df.loc[str(self.start_year):str(self.end_year)]
            m_vals = pd.DataFrame(index=df_.index.strftime('%Y'), columns = ['nday', 'value'])
            m_vals.index = pd.to_numeric(m_vals.index)
            deltas = []
            for date in df_.index:
                new_timestamp = pd.to_datetime('1704-'+date.strftime('%m-%d'))
                delta = (new_timestamp - self.scaletime).days
                deltas.append(delta)
            m_vals['nday'] = deltas
            m_vals['value'] = df_.values
        else:
            m_vals = pd.DataFrame(columns=['nday', 'value'])
            for year in self.years:
                md = self.df[varname].loc[str(year)].max() if mode == 'max' else self.df[varname].loc[str(year)].min()
                mindex = self.df[varname].loc[str(year)] == md
                df_ = pd.DataFrame(index=self.df.loc[str(year)][mindex].index, columns = ['nday', 'value'])
                deltas = []
                for date in df_.index:
                    new_timestamp = pd.to_datetime('1704-'+date.strftime('%m-%d'))
                    delta = (new_timestamp - self.scaletime).days
                    deltas.append(delta)
                m_vals = pd.concat([m_vals, pd.DataFrame({'nday': deltas, 'value': [md]*len(deltas)}, index=[year]*len(deltas))])
        m_vals['nday'] = pd.to_numeric(m_vals['nday'])
        m_vals['value'] = pd.to_numeric(m_vals['value'])
        
        if linreg == True:                              
            ddiv = (start_month-1)*30
            mvals_new = np.zeros(shape=(len(m_vals.index), len(m_vals.columns)))
            for i,nday in enumerate(m_vals.nday):
                mvals_new[i,0] = nday - ddiv if nday >= ddiv else nday - ddiv + 366
            mvals_new[:,1] = m_vals['value']
            m_vals = pd.DataFrame(mvals_new, index=m_vals.index, columns = ['nday', 'value'])
        return(m_vals)
    
    
    def get_mgrid(self, mode):
        """
        Function for monthly time-series
        Arguments:
            off: off-set a number of years from circle center (default in plot-function is 0)
            mode: aggregate data to monthly values ('sum', 'mean', 'max', 'min'); default = 'all' assumes that data is already in monthly resolution
        Returns:
            Dataframe for grid plot of monthly data
        """
        varname = self.df.columns[0]
        if mode == 'all':
            m_data = self.df
        else:
            df_ym = pd.DataFrame({varname: self.df[varname].values, 'yearmonth': self.df.index.strftime('%Y-%m')})
            if mode == 'sum':
                m_data = df_ym.groupby('yearmonth').sum()
            elif mode == 'mean':
                m_data = df_ym.groupby('yearmonth').mean()
            elif mode == 'min':
                m_data = df_ym.groupby('yearmonth').min()
            elif mode == 'max':
                m_data = df_ym.groupby('yearmonth').max()
            else:
                raise ValueError('"mode" for monthly data must be "all", "sum", "mean", "min" or "max".')
        m_data.index = pd.to_datetime(m_data.index, format='%Y-%m')            
        mgrid_data = np.empty(shape=(len(self.years), len(self.months)))
        for i,year in enumerate(self.years):
            mgrid_data[i,:] = m_data[varname].loc[str(year)].values
        mgrid_data = pd.DataFrame(mgrid_data, index=self.years, columns=self.months)        
        return(mgrid_data)
        
    
        
    def sp_plot(self, mode='all', label=None, rd_years = True, col = 'viridis_r', a = 1, psize= None, pmarker = None, nylabels=10, off=0, rlab_angle = 15, linreg = False, start_month = 1):
        """
        Plot function for seasonality polar plots. 
        Arguments:
            label: if rd_years = True this is the label for the colorbar legend, else it completes the labels of the radius axis
            rd_years: default = 'True' plots years on the radius axis, if 'False' plot years as circular lines and variable on radius axis
            col: color gradient (default 'viridis_r')
            a: transperancy alpha (0-1), 
            psize: marker size 
            pmarker: marker style 
            nylabels: number of (year) labels in radius direction
            off: off-set from circle center (default = 0)
            rlab_angle: angle of the radius axis labels
            linreg: default False, if True: plot linear regression in polar projection
            start_month: start month for linear regression of days in year
        """
        fig = plt.figure(dpi=125)
        ax = fig.add_subplot(projection='polar')
        ax.set_theta_direction(-1)
        ax.set_theta_zero_location('N')
        
        if rd_years == False:
            data = self.get_ev(mode)
            x = self.t_theta(data['nday'])
            y = data['value']
            colors = pd.DataFrame({'Col': sns.color_palette(col, len(self.years)).as_hex()}, index = self.years)
            for year in self.years:
                ax.plot(x[year], y[year], color=colors['Col'][year], label=year, zorder=-5)
            ax.legend(bbox_to_anchor=(1.3, 1.0), bbox_transform=ax.transAxes)
            ax.set_ylim(min(y)-off, max(y) + (max(y)-min(y))*0.1)
            rmax = max(data['value'])
            order = math.floor(math.log(rmax, 10))
            dec = order*(-1) if order < 0 else 0          
            yt = np.linspace(np.round(min(data['value']), dec), np.round(max(data['value']), dec), nylabels)
            if not label == None:
                yts = [str("%.{0}f".format(dec) % y)+label for y in yt]
                ax.set_rgrids(np.linspace(min(y), max(y), nylabels), labels=yts, fontsize=10, angle=rlab_angle)
                ax.set_yticklabels(yts, horizontalalignment = "center", verticalalignment = "center")
            
        elif self.t_res == 'daily':
            data = self.get_ev(mode, linreg, start_month)
            x = self.t_theta(data['nday'])
            y = data.index
            im = ax.scatter(x, y, c=data['value'], cmap=col, alpha=a, s=psize, marker=pmarker)
            ax.set_ylim(min(y)-off, max(y) + (max(y)-min(y))*0.1)
            yt = np.linspace(self.start_year, self.end_year, nylabels)
            yts = [str(int(y)) for y in yt]
            ax.set_rgrids(np.linspace(self.start_year, self.end_year, nylabels), labels=yts, fontsize=10, angle=rlab_angle)
            ax.set_yticklabels(yts, horizontalalignment = "center", verticalalignment = "center")
            fig.colorbar(im, ax=ax, label=label, pad=0.2)
           
        elif self.t_res == 'monthly':
            data = self.get_mgrid(mode)
            years_off = pd.DataFrame(index = list(range(self.start_year-off, self.start_year)), columns= data.columns)
            m_dat = pd.concat([years_off, data]) 
            theta = np.array(len(m_dat)*[np.linspace(0, 2*np.pi,13)]).T
            r = np.array(13*[np.linspace(m_dat.index[0]+0.5, m_dat.index[-1]+0.5, len(m_dat))])
            z = m_dat.T.values
            z = np.vstack([z, np.empty(shape=(1,len(m_dat)))])
            z[-1,:] = np.nan
            z = np.ma.masked_where(np.isnan(z),z)
            ax.grid(False)
            ax.set_ylim(m_dat.index[0]-0.5, m_dat.index[-1]+1)
            pos=ax.get_rlabel_position()
            ax.set_rlabel_position(pos-10)
            im = ax.pcolormesh(theta, r, z, cmap = col, shading='nearest')
            fig.colorbar(im, ax=ax, label=label, pad=0.2)
           
        if linreg == True:
            if self.t_res == 'monthly':
                raise ValueError('No linreg for monthly time series.')
            elif rd_years == False:
                raise ValueError('Use rd_years = True for linreg.')
            count = start_month - 1
            order = [x+count if (x+count) < 12 else x+count-12 for x in list(range(12))]
            months = [self.months[x] for x in order]
            b, a = np.polyfit(data.index, data['nday'], deg=1)
            xseq = np.linspace(min(data.index), max(data.index), num=500)
            yseq = a + b * xseq
            yseq_scale = self.t_theta(yseq)
            ax.plot(yseq_scale, xseq, color='k', lw=1.5)
            ax.arrow(yseq_scale[-2], xseq[-2], dx= (yseq_scale[-1] - yseq_scale[-2]), dy = (xseq[-1] - xseq[-2]), width = 0.01, head_width = 0.075, head_length = 2.5)
            reg = linregress(data.index, data['nday'])
            dof = 1.0*len(data) - 2
            t_intercept = reg.intercept/reg.intercept_stderr
            p_intercept = 2*t.sf(abs(t_intercept), dof)
            print('R2 = {0}, p_slope = {1}, p_intercept = {2}'.format(reg.rvalue**2, reg.pvalue, p_intercept))
        else:
            months = self.months
        ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
        ax.set_xticklabels(months, fontsize=10)



        
    def von_mises(self, mode, plot=True, print_par = True, bins=15, col_hist = 'b', col_vm ='r', off = 0.1, a = 1, rwidth = 0.8):
        """
        Function to plot and fit von Mises distribution of seasonal data (fitting with scipy vonmises gives Maximum Likelihood Estimates) 
        Arguments:
            mode: 'all' to use all data points, 'min' or 'max' to filter on extreme values
            plot: if True plots the data as circular histogram and fitted von Mises distribution
            bins: Number of bins for histogram
            col_hist: color of the histogram
            col_vm: color of the fitted von Mises distribution
            off: off-set from circle center
            rwidth: relative width of histogram bins
        """
        data = self.get_ev(mode)
        x = self.t_theta(data['nday'])
        kappa, mu, scale = vonmises.fit(x, fscale=1)
        mu_nday = int(mu*366/(2*np.pi))
        if plot == True:
            fig = plt.figure(dpi=125)
            ax = fig.add_subplot(projection='polar')
            ax.set_theta_direction(-1)
            ax.set_theta_zero_location('N')
            x_pred = np.linspace(0, 2*np.pi, num=500, endpoint=False)
            y_pred = np.exp(kappa*np.cos(x_pred-mu))/(2*np.pi*i0(kappa))
            ax.hist(x, bins=bins, density = True, color = col_hist, rwidth = rwidth, alpha = a)
            rmax = max(np.histogram(x, bins=bins, density=True)[0])
            ax.plot(x_pred, y_pred, color = col_vm)
            ax.set_xticks(np.linspace(0, 2*np.pi, 12, endpoint=False))
            ax.set_xticklabels(self.months, fontsize=10)
            ax.set_yticklabels([])
            ax.set_ylim(-off, rmax+0.1)
        if print_par == True:
            print('kappa = {0}, mu = {1}, mu_nday = {2}'.format(kappa, mu, mu_nday))
        else:
            return(kappa, mu, mu_nday)
       
