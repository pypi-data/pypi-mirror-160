#! /usr/bin/env python
#Standard python imports
import matplotlib
matplotlib.use("pdf")
import corner, h5py, matplotlib.pyplot as plt, numpy as np, os, sys, traceback, warnings
from matplotlib.ticker import FormatStrFormatter
from scipy.stats       import anderson, gaussian_kde
from scipy.signal      import tukey

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

#LVC imports
import lal
from lalinference      import DetFrameToEquatorial
from lalinference.imrtgr.nrutils import *

#Package internal imports
from pyRing.likelihood       import project
from pyRing.waveform         import *
from pyRing.utils            import bandpass_around_ringdown, compute_SNR_TD, compute_SNR_FD, import_datafile_path, qnm_interpolate, set_prefix, whiten_TD, whiten_FD



def init_plotting():
    
    plt.rcParams['figure.max_open_warning'] = 0
    
    plt.rcParams['figure.figsize']    = (5, 5)
    plt.rcParams['font.size']         = 10
    plt.rcParams['mathtext.fontset']  = 'stix'
    plt.rcParams['font.family']       = 'STIXGeneral'
    
    plt.rcParams['axes.linewidth']    = 1
    plt.rcParams['axes.labelsize']    = plt.rcParams['font.size']
    plt.rcParams['axes.titlesize']    = 1.5*plt.rcParams['font.size']
    plt.rcParams['legend.fontsize']   = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize']   = plt.rcParams['font.size']
    plt.rcParams['ytick.labelsize']   = plt.rcParams['font.size']
    plt.rcParams['xtick.major.size']  = 3
    plt.rcParams['xtick.minor.size']  = 3
    plt.rcParams['xtick.major.width'] = 1
    plt.rcParams['xtick.minor.width'] = 1
    plt.rcParams['ytick.major.size']  = 3
    plt.rcParams['ytick.minor.size']  = 3
    plt.rcParams['ytick.major.width'] = 1
    plt.rcParams['ytick.minor.width'] = 1
    
    plt.rcParams['legend.frameon']             = False
    plt.rcParams['legend.loc']                 = 'center left'
    plt.rcParams['contour.negative_linestyle'] = 'solid'
    
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.gca().yaxis.set_ticks_position('left')

def get_param_override(fixed_params,x,name):
    """
        Function returning either a sample or the fixed value for the parameter considered.
        ---------------
        
        Returns x[name], unless it is over-ridden by
        value in the fixed_params dictionary.
        
    """
    if name in fixed_params: return fixed_params[name]
    else:                    return x[name]

def FindHeightForLevel(inArr, adLevels):

    # flatten the array
    oldshape = np.shape(inArr)
    adInput= np.reshape(inArr,oldshape[0]*oldshape[1])
    # GET ARRAY SPECIFICS
    nLength = np.size(adInput)
    # CREATE REVERSED SORTED LIST
    adTemp = -1.0 * adInput
    adSorted = np.sort(adTemp)
    adSorted = -1.0 * adSorted
    # CREATE NORMALISED CUMULATIVE DISTRIBUTION
    adCum = np.zeros(nLength)
    adCum[0] = adSorted[0]
    for i in range(1,nLength):
        adCum[i] = np.logaddexp(adCum[i-1], adSorted[i])
    adCum = adCum - adCum[-1]
    # FIND VALUE CLOSEST TO LEVELS
    adHeights = []
    for item in adLevels:
        idx=(np.abs(adCum-np.log(item))).argmin()
        adHeights.append(adSorted[idx])
    adHeights = np.array(adHeights)

    return np.sort(adHeights)

def plot_contour(samples_stacked, level=[0.9], linest = 'dotted', label= None, color='k', line_w=1.2):

    warnings.filterwarnings('ignore', category=RuntimeWarning)

    kde         = gaussian_kde(samples_stacked.T)
    x_flat      = np.r_[samples_stacked[:,0].min():samples_stacked[:,0].max():128j]
    y_flat      = np.r_[samples_stacked[:,1].min():samples_stacked[:,1].max():128j]
    X,Y         = np.meshgrid(x_flat,y_flat)
    grid_coords = np.append(X.reshape(-1,1),Y.reshape(-1,1),axis=1)
    pdf         = kde(grid_coords.T)
    pdf         = pdf.reshape(128,128)
    hs  = []
    lgs = []
    for l in level:
        cntr       = plt.contour(X,Y,np.log(pdf),levels = np.sort(FindHeightForLevel(np.log(pdf),[l])), colors=color, linewidths=line_w, linestyles=linest)
        h,_ = cntr.legend_elements()
        hs.append(h[0])
        if not(label==None):
            lgs.append(r'${0} - {1} \% \, CI$'.format(label,int(l*100.)))
        else:
            lgs.append(r'${0} \% \, CI$'.format(int(l*100.)))
    plt.legend([h_x for h_x in hs], [lg for lg in lgs], loc='upper left')

    warnings.filterwarnings('default', category=RuntimeWarning)


def plot_strain(get_waveform, dets, fixed_params, tgps, params = None, whiten_flag = False, whiten_method = 'TD', strain_only = 0, **kwargs):

    if((strain_only==1) and (whiten_method == 'TD')): raise Exception('TD whitening requires a start time, which is not provided in `strain_only=1` mode.')

    init_plotting()
    model_waveforms = {d: [] for d in list(dets.keys())}
    dt_dict         = {d: [] for d in list(dets.keys())}
    if((whiten_method=='TD') and (kwargs['truncate']==1)): timeseries_whitened_TD = {d: [] for d in list(dets.keys())}
    ref_det         = kwargs['ref-det']
    tevent          = kwargs['trigtime']
    srate           = kwargs['sampling-rate']
    sky_frame       = kwargs['sky-frame']
    dt              = 1./srate
    duration_n      = kwargs['analysis-duration-n']

    #If there is no injected Mf, get an estimate of final mass from the tau of a chif=0.7 BH, for plotting purposes only.
    if(not(kwargs['injection-approximant']=='Damped-sinusoids') and not(kwargs['injection-approximant']=='')):
        mf_time_prior = kwargs['injection-parameters']['Mf']
    elif(kwargs['injection-approximant']=='Damped-sinusoids'):
        mf_time_prior = ((kwargs['injection-parameters']['tau']['t'][0]*lal.C_SI**3)/lal.G_SI)/(lal.MSUN_SI*20.)
    else:
        mf_time_prior = kwargs['mf-time-prior']

    if not(strain_only):
        for p in params:
            if p is not None:
                
                # Select sky position parameters
                if ('t' in fixed_params): t_start = fixed_params['t']
                else:                     t_start = p['t0']
                if (sky_frame == 'detector'):
                    non_ref_det  = kwargs['nonref-det']
                    cos_altitude = get_param_override(fixed_params,p,'cos_altitude')
                    azimuth      = get_param_override(fixed_params,p,'azimuth')
                    tg, ra, dec  = DetFrameToEquatorial(dets[ref_det].lal_detector, dets[non_ref_det].lal_detector, tevent, np.arccos(cos_altitude), azimuth)
                elif (sky_frame == 'equatorial'):
                    ra  = get_param_override(fixed_params,p,'ra')
                    dec = get_param_override(fixed_params,p,'dec')
                else:
                    if (len(dets) > 1):
                        non_ref_det  = kwargs['nonref-det']
                        cos_altitude = get_param_override(fixed_params,p,'cos_altitude')
                        azimuth      = get_param_override(fixed_params,p,'azimuth')
                        tg, ra, dec  = DetFrameToEquatorial(dets[ref_det].lal_detector, dets[non_ref_det].lal_detector, tevent, np.arccos(cos_altitude), azimuth)
                    else:
                        ra  = get_param_override(fixed_params,p,'ra')
                        dec = get_param_override(fixed_params,p,'dec')
                psi = get_param_override(fixed_params,p,'psi')

                # Generate waveform
                waveform_polarisations = get_waveform(p)
                for d in list(dets.keys()):
                    detector             = dets[d]
                    time_delay           = lal.ArrivalTimeDiff(detector.location, lal.cached_detector_by_prefix[ref_det].location, ra, dec, tgps)
                    time_array           = detector.time - (tevent+time_delay)
                    hs, hvx, hvy, hp, hc = waveform_polarisations.waveform(time_array)
                    waveform_proj        = project(hs, hvx, hvy, hp, hc, detector.lal_detector, ra, dec, psi, tgps)

                    if whiten_flag:
                        waveform_proj = bandpass_around_ringdown(waveform_proj, dt, kwargs['f-min-bp'], mf_time_prior, alpha_window=0.1)
                        if(  whiten_method=='FD'):
                            waveform = whiten_FD(waveform_proj, detector.psd, dt, kwargs['f-min-bp'], kwargs['f-max-bp'])
                        elif(whiten_method=='TD'):

                            # In the case where we truncate and use the TD domain, the whitening depends on when the analysis starts, i.e. the samples. Hence, the whitened data will be different depending on the sample.
                            if(kwargs['truncate']==1):
                                waveform_proj = waveform_proj[time_array >= t_start][:duration_n]
                                
                                timeseries_tmp = bandpass_around_ringdown(detector.time_series, dt, kwargs['f-min-bp'], mf_time_prior, alpha_window=0.1)
                                timeseries_tmp = timeseries_tmp[time_array >= t_start][:duration_n]
                                timeseries_tmp = whiten_TD(timeseries_tmp, detector.cholesky)
                                timeseries_whitened_TD[d].append(timeseries_tmp)
                            
                            waveform = whiten_TD(waveform_proj, detector.cholesky)
                    
                        else:
                            raise ValueError('Unknown whitening method requested.')
                    else:
                        waveform = waveform_proj
                    
                    model_waveforms[d].append(waveform)
                    dt_dict[d].append(time_delay+t_start)
            else:
                waveform_polarisations = None

    nsub_panels = len(dets)
    
    #########################
    # Data vs waveform plot #
    #########################
    
    if(strain_only): filename = 'strain'
    else:            filename = 'reconstructed_waveform'
    fig = plt.figure()
    # Plot the data
    for i,d in enumerate(dets.keys()):
        detector = dets[d]
        ax = fig.add_subplot(nsub_panels,1,i+1)
        if whiten_flag:
            
            if(whiten_method=='FD'):
                timeseries_tmp = bandpass_around_ringdown(detector.time_series, dt, kwargs['f-min-bp'], mf_time_prior, alpha_window=0.1)
                timeseries     = whiten_FD(timeseries_tmp, detector.psd, dt, kwargs['f-min-bp'], kwargs['f-max-bp'])
                time_axis      = detector.time-tevent
            elif(whiten_method=='TD'):
    
                if(kwargs['truncate']==1):
                    timeseries_regions = np.percentile(np.array(timeseries_whitened_TD[d]),[5,50,95], axis=0)
                    timeseries         = timeseries_regions[1]
                    dt_regions         = np.percentile(np.array(dt_dict[d]),[5,50,95], axis=0)
                    time_axis          = (detector.time-tevent-dt_regions[1])
                    time_axis          = time_axis[time_axis >= 0][:duration_n]

                else:
                    timeseries = bandpass_around_ringdown(detector.time_series, dt, kwargs['f-min-bp'], mf_time_prior, alpha_window=0.1)
                    timeseries = whiten_TD(timeseries, detector.cholesky)
                    time_axis  = detector.time-tevent
            else:
                raise ValueError('Unknown whitening method requested.')

            wtleg      = 'whitened'
            label_y    = r'$\mathrm{s_{%s}(t)}$'%(d)
            ax.set_ylim([-5,5])
        else:
            timeseries = detector.time_series
            time_axis  = detector.time-tevent
            wtleg      = ''
            label_y    = r'$\mathrm{Strain}$'
        ax.plot(time_axis, timeseries, label='{}'.format(d)+' strain '+wtleg, c='black', linestyle='-', lw=1.0)
        ax.set_ylabel(label_y)
        if (d=='H1' and (nsub_panels > 1)):
            ax.get_xaxis().set_visible(False)
            ax.grid(False)
        
        if not(strain_only):
            # Plot waveform median and 90% region
            waveform_regions = np.percentile(np.array(model_waveforms[d]),[5,50,95], axis=0)
            dt_regions       = np.percentile(np.array(dt_dict[d]),[5,50,95], axis=0)
            ax.plot(time_axis, waveform_regions[1], label='model '+wtleg, color='gold', lw=0.8)
            ax.fill_between(time_axis, waveform_regions[0], waveform_regions[2], facecolor='gold', lw=0.5, alpha=0.4)
            try:
                if(  whiten_method=='FD'):
                    ax.set_xlim([dt-150*mf_time_prior*lal.MTSUN_SI, dt+80*mf_time_prior*lal.MTSUN_SI])
                    ax.axvline(0.0, c='deeppink', linestyle='dashed', lw=1.0, label=r'$\mathrm{t_{start}}$')
                elif(whiten_method=='TD'):
                    ax.set_xlim([0.0, dt+150*mf_time_prior*lal.MTSUN_SI])
            except (KeyError,configparser.NoOptionError, configparser.NoSectionError):
                print("\nWarning: Failed to complete strain plot due to error: {}.".format(traceback.print_exc()))
        ax.legend(loc='upper left', prop={'size': 6})
        ax.set_xlabel('Time [s]')
    plt.grid(False)
    plt.subplots_adjust(wspace=0, hspace=0)
    if not(wtleg==''): filename = filename + '_' + wtleg + '_{}'.format(whiten_method)
    plt.savefig(os.path.join(kwargs['output'],'Plots/Strains', filename+'.pdf'), bbox_inches='tight')


    if(whiten_flag and not(strain_only)):

        ##################
        # Residuals plot #
        ##################

        fig = plt.figure()
        # Plot the data
        for i,d in enumerate(dets.keys()):
            detector = dets[d]
            ax = fig.add_subplot(nsub_panels,1,i+1)
            
            if(whiten_method=='FD'):
                timeseries_tmp = bandpass_around_ringdown(detector.time_series, dt, kwargs['f-min-bp'], mf_time_prior, alpha_window=0.1)
                timeseries     = whiten_FD(timeseries_tmp, detector.psd, dt, kwargs['f-min-bp'], kwargs['f-max-bp'])
                time_axis      = detector.time-tevent
            elif(whiten_method=='TD'):
    
                if(kwargs['truncate']==1):
                    timeseries_regions = np.percentile(np.array(timeseries_whitened_TD[d]),[5,50,95], axis=0)
                    timeseries         = timeseries_regions[1]
                    dt_regions         = np.percentile(np.array(dt_dict[d]),[5,50,95], axis=0)
                    time_axis          = (detector.time-tevent-dt_regions[1])
                    time_axis          = time_axis[time_axis >= 0][:duration_n]

                else:
                    timeseries = bandpass_around_ringdown(detector.time_series, dt, kwargs['f-min-bp'], mf_time_prior, alpha_window=0.1)
                    timeseries = whiten_TD(timeseries, detector.cholesky)
                    time_axis  = detector.time-tevent
            else:
                raise ValueError('Unknown whitening method requested.')

            label_y    = r'$\mathrm{s_{%s}(t)}$'%(d)

            ax.set_ylabel(label_y)
            if (d=='H1' and (nsub_panels > 1)):
                ax.get_xaxis().set_visible(False)
                ax.grid(False)
            
            # Plot waveform median and 90% region
            waveform_regions = np.percentile(np.array(model_waveforms[d]),[5,50,95], axis=0)
            
            residuals_median = timeseries-waveform_regions[1]
            residuals_lower  = timeseries-waveform_regions[0]
            residuals_upper  = timeseries-waveform_regions[2]

            ax.plot(time_axis, residuals_median, label='whitened residuals', color='gold', lw=0.8)
            ax.axhline(1.0,  c='black',   linestyle='dotted', lw=0.6, label=r'$\pm 1 \sigma$')
            ax.axhline(-1.0, c='black',   linestyle='dotted', lw=0.6)
            ax.axhline(2.0,  c='darkred', linestyle='dotted', lw=0.6, label=r'$\pm 2 \sigma$')
            ax.axhline(-2.0, c='darkred', linestyle='dotted', lw=0.6)
            ax.fill_between(time_axis, residuals_lower, residuals_upper, facecolor='gold', lw=0.5, alpha=0.4)
            try:
                if(  whiten_method=='FD'):
                    ax.set_ylim([-5,5])
                    ax.set_xlim([dt-150*mf_time_prior*lal.MTSUN_SI, dt+80*mf_time_prior*lal.MTSUN_SI])
                    ax.axvline(0.0, c='deeppink', linestyle='dashed', lw=1.0, label=r'$\mathrm{t_{start}}$')
                elif(whiten_method=='TD'):
                    ax.set_ylim([-3,3])
                    ax.set_xlim([0.0, dt+150*mf_time_prior*lal.MTSUN_SI])
            except (KeyError,configparser.NoOptionError, configparser.NoSectionError):
                print("\nWarning: Failed to complete strain plot due to error: {}.".format(traceback.print_exc()))
            ax.legend(loc='upper left', prop={'size': 6})
            ax.set_xlabel('Time [s]')
        plt.grid(False)
        plt.subplots_adjust(wspace=0, hspace=0)
        if not(wtleg==''): filename = 'whitened_residuals' +'_{}'.format(whiten_method)
        plt.savefig(os.path.join(kwargs['output'],'Plots/Strains', filename+'.pdf'), bbox_inches='tight')


        if(whiten_method=='TD'):

            # Plot whitened residuals against a normal distribution, to visually check gaussianity.
            
            # FIXME: this number should be experimented with.
            nbins = 50
            normal_draws = np.random.normal(size=1000000)

            # Plot the data
            for i,d in enumerate(dets.keys()):
                detector = dets[d]
                fig = plt.figure()

                label_y    = r'$\mathrm{s_{%s}(t)}$'%(d)
                plt.ylabel(label_y)

                for i in range(len(model_waveforms[d])):
                    plt.hist(timeseries_whitened_TD[d][i]-model_waveforms[d][i], histtype='step', bins=nbins, stacked=True, fill=False, density=True, color='gold', lw=0.5, alpha=0.4)

                gaussian_x, bins_gauss, _ = plt.hist(normal_draws, label='Expected distribution', histtype='step', bins=nbins, stacked=True, fill=False, density=True, color='black', linewidth=2.0)
# Work in progress
#                sigma                     = [gaussian_x[i]*(1-gaussian_x[i]) for i in range(len(gaussian_x))]
#                lower, upper              = gaussian_x - sigma, gaussian_x + sigma
#                plt.plot(bins_gauss[:-1], lower, color='black', linewidth=1.7, linestyle='dashed')
#                plt.plot(bins_gauss[:-1], upper, color='black', linewidth=1.7, linestyle='dashed')
                
                plt.legend(loc='best')
                plt.xlabel('Whitened residuals')
                plt.savefig(os.path.join(kwargs['output'],'Plots/Strains','Histrogram_whitened_residuals_{}_{}.pdf'.format(d, whiten_method)), bbox_inches='tight')

                # Now let's compute a quantitative measure of gaussianity.
                AD_statistics = []
                for i in range(len(model_waveforms[d])):
                    AD_statistic, critical_values, significance_level = anderson(timeseries_whitened_TD[d][i]-model_waveforms[d][i], dist='norm')
                    AD_statistics.append(AD_statistic)

                AD_statistics = np.array(AD_statistics)
                mask_outliers = AD_statistics > critical_values[-1]
                N_outliers    = len(AD_statistics[mask_outliers])
                len_tot       = len(AD_statistics)
                n, bins, _    = plt.hist(AD_statistics)
                bin_width     = bins[1] - bins[0]
                integral      = bin_width * sum(n)

                plt.figure()
                plt.hist(AD_statistics, histtype='step', bins=nbins, stacked=True, fill=False, color='black', linewidth=2.0)
                plt.axvline(critical_values[-1], label = 'Significance level: {}\nN outliers: {}/{}'.format(significance_level[-1], N_outliers, len_tot), color='darkred', linestyle='dashed', linewidth=1.5)
                plt.xlabel('Anderson-Darling statistic')
                plt.title('Integral: {:.6f}'.format(integral))
                plt.legend(loc='upper right')
                plt.savefig(os.path.join(kwargs['output'],'Plots/Strains',' Histogram_Anderson_Darling_statistic_whitened_residuals_{}_{}.pdf'.format(d, whiten_method)), bbox_inches='tight')

                plt.figure()
                plt.scatter(np.arange(0,len(AD_statistics)), AD_statistics, color='black', marker='x')
                plt.axhline(critical_values[-1], label = 'Significance level: {}\nN outliers: {}/{}'.format(significance_level[-1], N_outliers, len_tot), color='darkred', linestyle='dashed', linewidth=1.5)
                plt.xlabel('Samples')
                plt.ylabel('Anderson-Darling statistic')
                plt.ylim([0,2])
                plt.legend(loc='upper right')
                plt.savefig(os.path.join(kwargs['output'],'Plots/Strains',' Scatter_Anderson_Darling_statistic_whitened_residuals_{}_{}.pdf'.format(d, whiten_method)), bbox_inches='tight')

                print('* Anderson-Darling statistic of whitened {} residuals gave {}/{} normality outliers (at {} % significance).\n'.format(d, N_outliers, len_tot, significance_level[-1]))

    return

def SNR_plots(get_waveform, dets, fixed_params, tgps, params = None, **kwargs):

    # Initialise plotting.
    init_plotting()
    
    # Initialise structures.
    SNRs, network_SNRs = {}, {}
    
    # Read auxiliary quantities.
    ref_det           = kwargs['ref-det']
    tevent            = kwargs['trigtime']
    srate             = kwargs['sampling-rate']
    sky_frame         = kwargs['sky-frame']
    seglen            = np.int(srate*kwargs['signal-chunksize'])
    dt                = 1./srate
    freqs             = np.fft.rfftfreq(seglen, d=dt)
    df                = freqs[1] - freqs[0]
    duration_n        = kwargs['analysis-duration-n']
    alpha_window      = kwargs['alpha-window']
    likelihood_method = kwargs['likelihood-method']
    
    domain            = 'TD'
    
    print('Medians:\n')
    
    # Loop on TD/FD computation and type of SNR.
    
    SNRs[domain]         = {}
    network_SNRs[domain] = {}
    
    for SNR_type in ['matched_filter', 'optimal']:
        
        SNRs[domain][SNR_type]         = {d: [] for d in list(dets.keys())}
        network_SNRs[domain][SNR_type] = []

        # Loop on posterior samples.
        for p in params:

            # Read time and sky position parameters, required separately to compute truncated time axis.
            if ('t' in fixed_params): t_start = fixed_params['t']
            else:                     t_start = p['t0']
            if (sky_frame == 'detector'):
                non_ref_det = kwargs['nonref-det']
                cos_altitude = get_param_override(fixed_params,p,'cos_altitude')
                azimuth      = get_param_override(fixed_params,p,'azimuth')
                tg, ra, dec = DetFrameToEquatorial(dets[ref_det].lal_detector, dets[non_ref_det].lal_detector, tevent, np.arccos(cos_altitude), azimuth)
            elif (sky_frame == 'equatorial'):
                ra  = get_param_override(fixed_params,p,'ra')
                dec = get_param_override(fixed_params,p,'dec')
            else:
                if (len(dets) > 1):
                    non_ref_det = kwargs['nonref-det']
                    cos_altitude = get_param_override(fixed_params,p,'cos_altitude')
                    azimuth      = get_param_override(fixed_params,p,'azimuth')
                    tg, ra, dec = DetFrameToEquatorial(dets[ref_det].lal_detector, dets[non_ref_det].lal_detector, tevent, np.arccos(cos_altitude), azimuth)
                else:
                    ra  = get_param_override(fixed_params,p,'ra')
                    dec = get_param_override(fixed_params,p,'dec')
            psi = get_param_override(fixed_params,p,'psi')

            # Generate waveform polarisations.
            waveform_polarisations = get_waveform(p)

            # Loop onto detectors.
            for d in list(dets.keys()):
                
                # Compute detector time axis.
                detector      = dets[d]
                time_delay    = lal.ArrivalTimeDiff(detector.location, lal.cached_detector_by_prefix[ref_det].location, ra, dec, tgps)
                time_array    = detector.time - (tevent+time_delay)

                # Compute polarisations.
                data_TD = detector.time_series

                if(domain=='FD'):
                    window               = tukey(seglen,alpha_window)
                    windowNorm           = seglen/np.sum(window**2)
                    data                 = np.real(np.fft.rfft(data_TD*window*dt))*windowNorm
                
                    hs, hvx, hvy, hp, hc = waveform_polarisations.waveform(time_array)
                    waveform_TD_tmp      = project(hs, hvx, hvy, hp, hc, detector.lal_detector, ra, dec, psi, tgps)
                    waveform             = np.real(np.fft.rfft(waveform_TD_tmp*dt))
                
                elif(domain=='TD'):
                    if(kwargs['truncate']==1):
                        data             = data_TD[time_array >= t_start][:duration_n]
                        time_array       = time_array[time_array >= t_start][:duration_n]
                    else:
                        data             = data_TD
                    hs, hvx, hvy, hp, hc = waveform_polarisations.waveform(time_array)
                    waveform             = project(hs, hvx, hvy, hp, hc, detector.lal_detector, ra, dec, psi, tgps)

                # Compute inner product weights.
                if(  domain=='FD'):
                    weights_FD = detector.psd(freqs)
                    if(SNR_type=='optimal'):          SNR_sample = compute_SNR_FD(waveform, waveform, weights_FD, df)
                    elif(SNR_type=='matched_filter'): SNR_sample = compute_SNR_FD(data,     waveform, weights_FD, df)
                elif(domain=='TD'):
                    TD_method = likelihood_method
                    if(  TD_method=='direct-inversion'         ): weights_TD = detector.inverse_covariance
                    elif(TD_method=='cholesky-solve-triangular'): weights_TD = detector.cholesky
                    elif(TD_method=='toeplitz-inversion'       ): weights_TD = detector.acf
                    
                    if(SNR_type=='optimal'):          SNR_sample = compute_SNR_TD(waveform, waveform, weights_TD, method=TD_method)
                    elif(SNR_type=='matched_filter'): SNR_sample = compute_SNR_TD(data,     waveform, weights_TD, method=TD_method)

                # Store SNR sample.
                SNRs[domain][SNR_type][d].append(SNR_sample)

            # Compute network SNR.
            network_SNRs[domain][SNR_type].append(np.sqrt(np.sum([SNRs[domain][SNR_type][d][-1]**2 for d in list(dets.keys())])))

        # Plot the results.
        SNR_header    = 'Network\t'
        SNR_filestack = (network_SNRs[domain][SNR_type],)

        print('Network {} SNR ({}): {:.3f}'.format(SNR_type.ljust(len('matched_filter')), domain, np.median(network_SNRs[domain][SNR_type])))

        for d in list(dets.keys()):
            SNR_header += '{}\t'.format(d)
            SNR_filestack  = SNR_filestack  + (SNRs[domain][SNR_type][d],)
            print('{} {} SNR ({}): {:.3f}'.format(d.ljust(len('Network')), SNR_type.ljust(len('matched_filter')), domain, np.median(SNRs[domain][SNR_type][d])))
            plt.figure()
            plt.hist(SNRs[domain][SNR_type][d], histtype='step', bins=70, stacked=True, fill=False, density=True, label = '{} SNR (TD)'.format(d))
            plt.savefig(os.path.join(kwargs['output'],'Plots', 'SNR/{}_{}_SNR_{}.pdf'.format(d, SNR_type, domain)), bbox_inches='tight')
        plt.figure()
        plt.hist(network_SNRs[domain][SNR_type], histtype='step', bins=70, stacked=True, fill=False, density=True, label = 'Network SNR ({})'.format(domain))
        plt.savefig(os.path.join(kwargs['output'],'Plots', 'SNR/{}_network_SNR_{}.pdf'.format(SNR_type, domain)), bbox_inches='tight')
        np.savetxt(os.path.join(kwargs['output'],'Nested_sampler/{}_SNR_{}.dat'.format(SNR_type, domain)), np.column_stack(SNR_filestack), header=SNR_header)

    return

def mode_corner(samples,filename=None,**kwargs):
    
    fig = plt.figure(figsize=(10,10))
    C   = corner.corner(samples,**kwargs)
    if filename is not None: plt.savefig(filename,bbox_inches='tight')
    
    return fig

def f0_t0_gr(samples, Mf_s, af_s, Num_mode, **kwargs):
    init_plotting()
    output_dir = os.path.join(kwargs['output'], 'Plots')
    
    # Initialise structures.
    theoretical_values, labels    = [], []
    qnm_interpolants              = {}
    i, Num_modes, delta_QNM_plots = 0, 0, 0
    
    #IMPROVEME: Colours for generic N modes, now it's hardcoded for 12 modes.
    n_values = [0]
    l_values = [2,3]
    for l in l_values:
        Num_modes += len(n_values)*(2*l+1)
    print('\n* Total number of modes used to produce frequency-tau plots: {}\n'.format(Num_modes))
    colors_manual= [ 'green', 'forestgreen', 'mediumaquamarine', 'springgreen', 'aquamarine', 'khaki', 'yellow','gold', 'orange', 'orangered', 'red', 'firebrick']

    # Plot the GR prediction for frequency and damping time coming from an IMR run.
    fig=plt.figure()
    ax = plt.axes()
    for n in n_values:
        for l in l_values:
            for m in range(-l,l+1,1):
                col = colors_manual[i]
                if(kwargs['qnm-fit'] == 1):
                    qnm                               = QNM_fit(l,m,n)
                else:
                    interpolate_freq, interpolate_tau = qnm_interpolate(2,l,m,n)
                    qnm_interpolants[(2,l,m,n)]       = {'freq': interpolate_freq, 'tau': interpolate_tau}
                    qnm                               = QNM(2,l,m,n,qnm_interpolants)
                f0 = [qnm.f(M,a)       for M,a in zip(Mf_s,af_s)]
                t0 = [1e3*qnm.tau(M,a) for M,a in zip(Mf_s,af_s)]
                theoretical_values.append([f0,t0])
                labels.append(r'$(%d,%d,%d)$ '%(l,m,n))
                f0_t0_IMR   = np.column_stack((f0,t0))
                kde         = gaussian_kde(f0_t0_IMR.T)
                x_flat      = np.r_[f0_t0_IMR[:,0].min():f0_t0_IMR[:,0].max():128j]
                y_flat      = np.r_[f0_t0_IMR[:,1].min():f0_t0_IMR[:,1].max():128j]
                X,Y         = np.meshgrid(x_flat,y_flat)
                grid_coords = np.append(X.reshape(-1,1),Y.reshape(-1,1),axis=1)
                pdf         = kde(grid_coords.T)
                pdf         = pdf.reshape(128,128)
                pdf[np.where(pdf==0.)] = 1.e-100
                plt.contour(X,Y,np.log(pdf),levels = np.sort(FindHeightForLevel(np.log(pdf),[0.9])), colors=col, linewidths=2.0, linestyles='solid')
                i = i+1
                if(delta_QNM_plots):
                    difference_freq = np.array([(samples[j,0]-f0[k])/f0[k] for k in range(len(f0)) for j in range(0,samples.shape[0])])
                    difference_tau  = np.array([(samples[j,1]-t0[k])/t0[k] for k in range(len(t0)) for j in range(0,samples.shape[0])])
                    plt.figure()
                    plt.hist(difference_freq, histtype='step', bins=70, stacked=True, fill=False, normed=1)
                    plt.xlabel(r'$\mathrm{\delta f_{%d%d%d}}$'%(l,m,n))
                    plt.ylabel(r'$\mathrm{P(\delta f_{%d%d%d}|D)}$'%(l,m,n))
                    plt.savefig(os.path.join(output_dir,'dfreq_{}{}{}_{}.png'.format(l,m,n,Num_mode)) ,bbox_inches='tight')
                    plt.figure()
                    plt.hist(difference_tau, histtype='step', bins=70, stacked=True, fill=False, normed=1)
                    plt.xlabel(r'$\mathrm{\delta \tau_{%d%d%d}}$'%(l,m,n))
                    plt.ylabel(r'$\mathrm{P(\delta \tau_{%d%d%d}|D)}$'%(l,m,n))
                    plt.savefig(os.path.join(output_dir,'Parameters/dtau_{}{}{}_{}.png'.format(l,m,n,Num_mode)) ,bbox_inches='tight')

    # Plot the freq-tau 2-D posterior on top of GR predictions.
    kde         = gaussian_kde(samples.T)
    x_flat      = np.r_[samples[:,0].min():samples[:,0].max():128j]
    y_flat      = np.r_[samples[:,1].min():samples[:,1].max():128j]
    X,Y         = np.meshgrid(x_flat,y_flat)
    grid_coords = np.append(X.reshape(-1,1),Y.reshape(-1,1),axis=1)
    pdf         = kde(grid_coords.T)
    pdf         = pdf.reshape(128,128)
    plt.scatter(samples[:,0], samples[:,1], cmap='seismic',  marker='.', alpha=0.3, s=2)
    plt.contour(X, Y, np.log(pdf), levels = np.sort(FindHeightForLevel(np.log(pdf),[0.5,0.90])), colors='k', linestyles='solid')

    # Compute the probability that each of the modes is the one corresponding to the samples.
    # To understand why the kde evaluation on the samples, combined with the mean of the probability, is the correct procedure to compute this number, see TeX/Likelihood.tex
    theoretical_values = np.array(theoretical_values)
    probs              = np.array([kde(t) for t in theoretical_values])

    mprob = np.array([np.mean(probs[i,:]) for i in range(len(colors_manual))])
    mprob /= mprob.sum()
    import matplotlib.patches as mpatches
    patches = [mpatches.Patch(color=c, label = labels[i]+r'$p={} \%$'.format(int(100*mprob[i]))) for i,c in enumerate(colors_manual)]

    l = ax.legend(handles = patches,
                  fancybox       = True,
                  loc            = "upper right",
                  borderaxespad  = 0.,
                  fontsize       = 7)

    ax.set_xlabel(r'$\mathrm{f\,(Hz)}$')
    ax.set_ylabel(r'$\mathrm{\tau\, (ms)}$')
    plt.savefig(os.path.join(output_dir,'Parameters/frequency_tau_{}.pdf'.format(Num_mode)) ,bbox_inches='tight')
    return fig

def Kerr_intrinsic_corner(x, **input_par):

    # Corner plot of final mass and final spin
    pos             = np.column_stack((x['Mf'], x['af'], x['t0']))
    injected_values = None
    if (input_par['injection-approximant']=='Kerr'):
        injected_values = [input_par['injection-parameters']['Mf'], input_par['injection-parameters']['af'], input_par['injection-parameters']['t0']]
    mode_corner(  pos,
                  labels        = [r'$M_f (M_{\odot})$',
                                   r'$a_f$'            ,
                                   r'$t_{start}$'      ],
                  quantiles     = [0.05, 0.5, 0.95],
                  show_titles   = True,
                  title_kwargs  = {"fontsize": 12},
                  use_math_text = True,
                  truths        = injected_values,
                  filename      = os.path.join(input_par['output'],'Plots/Parameters/Kerr_intrinsic_corner.png'))

def Kerr_intrinsic_alpha_corner(x, **input_par):

    # Corner plot of final mass, final spin, and alpha
    try:
        pos             = np.column_stack((x['Mf'], x['af'], x['alpha']))
        injected_values = None
        if (input_par['inject-area-quantization']):
            injected_values = [input_par['injection-parameters']['Mf'], input_par['injection-parameters']['af'], input_par['injection-parameters']['alpha']]

        mode_corner(  pos,
                    labels        = [r'$M_f (M_{\odot})$',
                                     r'$a_f$'            ,
                                     r'$\alpha$'      ],
                    quantiles     = [0.05, 0.5, 0.95],
                    show_titles   = True,
                    title_kwargs  = {"fontsize": 12},
                    use_math_text = True,
                    truths        = injected_values,
                    filename      = os.path.join(input_par['output'],'Plots/Parameters/Kerr_intrinsic_alpha_corner.png'))
    except(ValueError):
        pass

def MMRDNS_intrinsic_corner(x, **input_par):

    pos             = np.column_stack( (x['Mf'], x['af'], x['eta'], x['t0']) )
    injected_values = None

    if (input_par['injection-approximant']=='NR'):
        M    = input_par['injection-parameters']['M']
        q    = input_par['injection-parameters']['q']
        eta = q/((1+q)*(1+q))
        injected_values = [input_par['injection-parameters']['Mf'], input_par['injection-parameters']['af'], eta, 12*input_par['injection-parameters']['M']*lal.MTSUN_SI]
    elif (input_par['injection-approximant']=='Kerr'):
        injected_values = [input_par['injection-parameters']['Mf'], input_par['injection-parameters']['af'], None, 12*input_par['injection-parameters']['Mf']*lal.MTSUN_SI]
    elif(input_par['injection-approximant']=='MMRDNS'):
        injected_values = [input_par['injection-parameters']['Mf'], input_par['injection-parameters']['af'], input_par['injection-parameters']['eta'], input_par['injection-parameters']['t0']]
    mode_corner(pos,
                labels        = [r'$M_f (M_{\odot})$',
                                 r'$a_f$'            ,
                                 r'$\eta$'           ,
                                 r'$t_{start}$'      ],
                quantiles     = [0.05, 0.5, 0.95],
                show_titles   = True,
                title_kwargs  = {"fontsize": 12},
                use_math_text = True,
                truths        = injected_values,
                filename      = os.path.join(input_par['output'],'Plots/Parameters/MMRDNS_intrinsic_corner.png'))

def MMRDNP_intrinsic_corner(x, **input_par):

    pos             = np.column_stack((x['m1'], x['m2'], x['chi1'], x['chi2']))
    injected_values = None

    if((input_par['injection-approximant']=='NR') or (input_par['injection-approximant']=='MMRDNP') or (input_par['injection-approximant']=='TEOBResumSPM') or ('LAL' in input_par['injection-approximant'])):

        injected_values = [input_par['injection-parameters']['m1'],
                           input_par['injection-parameters']['m2'],
                           input_par['injection-parameters']['chi1'],
                           input_par['injection-parameters']['chi2']]

    mode_corner(pos,
                labels        = [r'$m1 (M_{\odot})$',
                                 r'$m2 (M_{\odot})$',
                                 r'$\chi_1$'        ,
                                 r'$\chi_2$'        ],
                quantiles     = [0.05, 0.5, 0.95],
                show_titles   = True,
                title_kwargs  = {"fontsize": 12},
                use_math_text = True,
                truths        = injected_values,
                filename      = os.path.join(input_par['output'],'Plots/Parameters/MMRDNP_intrinsic_corner.png'))

def MMRDNP_amplitude_parameters_corner(x, **input_par):

    m1   = x['m1']
    m2   = x['m2']
    chi1 = x['chi1']
    chi2 = x['chi2']
    M    = m1 + m2
    q    = m1/m2
    chis = (m1*chi1 + m2*chi2)/M
    chia = (m1*chi1 - m2*chi2)/M
    eta  = q/((1+q)*(1+q))

    pos = np.column_stack((eta, chis, chia))
    injected_values = None

    if((input_par['injection-approximant']=='NR') or (input_par['injection-approximant']=='TEOBResumSPM') or ('LAL' in input_par['injection-approximant'])):

        M_inj    = input_par['injection-parameters']['M']
        q_inj    = input_par['injection-parameters']['q']
        m1_inj   = input_par['injection-parameters']['m1']
        m2_inj   = input_par['injection-parameters']['m2']
        if not(input_par['injection-approximant']=='TEOBResumSPM'):
            chi1_inj = input_par['injection-parameters']['s1z_LALSim']
            chi2_inj = input_par['injection-parameters']['s2z_LALSim']
        else:
            chi1_inj = input_par['injection-parameters']['chi1']
            chi2_inj = input_par['injection-parameters']['chi2']
        chis_inj = (m1_inj*chi1_inj + m2_inj*chi2_inj)/M_inj
        chia_inj = (m1_inj*chi1_inj - m2_inj*chi2_inj)/M_inj
        eta_inj  = q_inj/((1+q_inj)*(1+q_inj))

        injected_values = [eta_inj, chis_inj, chia_inj]

    elif(input_par['injection-approximant']=='MMRDNP'):

        injected_values = [input_par['injection-parameters']['eta'],
                           input_par['injection-parameters']['chis'],
                           input_par['injection-parameters']['chia']]

    mode_corner(pos,
                labels        = [r'$\eta$' ,
                                r'$\chi_s$',
                                r'$\chi_a$'],
                quantiles     = [0.05, 0.5, 0.95],
                show_titles   = True,
                title_kwargs  = {"fontsize": 12},
                use_math_text = True,
                truths        = injected_values,
                filename      = os.path.join(input_par['output'],'Plots/Parameters/MMRDNP_amplitude_parameters_corner.png'))

def MMRDNP_Mf_af_plot(x, **input_par):

    Mf = []
    af = []
    for par in x:
        if(par['chi1'] < 0): tilt1_fit = np.pi
        else: tilt1_fit = 0.0
        if(par['chi2'] < 0): tilt2_fit = np.pi
        else: tilt2_fit = 0.0
        chi1_fit  = np.abs(par['chi1'])
        chi2_fit  = np.abs(par['chi2'])
        Mf_x = bbh_final_mass_projected_spins(par['m1'], par['m2'], chi1_fit, chi2_fit, tilt1_fit, tilt2_fit, 'UIB2016')
        af_x = bbh_final_spin_projected_spins(par['m1'], par['m2'], chi1_fit, chi2_fit, tilt1_fit, tilt2_fit, 'UIB2016', truncate = bbh_Kerr_trunc_opts.trunc)
        Mf.append(Mf_x)
        af.append(af_x)

    pos             = np.column_stack((Mf, af))
    injected_values = None
    if not((input_par['injection-approximant']=='Damped-sinusoids') or (input_par['injection-approximant']=='Morlet-Gabor-wavelets')):
        injected_values = [input_par['injection-parameters']['Mf'], input_par['injection-parameters']['af']]

    mode_corner(pos,
                labels        = [r'$M_f (M_{\odot})$',
                                 r'$a_f$'            ],
                quantiles     = [0.05, 0.5, 0.95],
                show_titles   = True,
                title_kwargs  = {"fontsize": 12},
                use_math_text = True,
                truths        = injected_values,
                filename      = os.path.join(input_par['output'],'Plots/Parameters/MMRDNP_Mf_af_plot.png'))

def orientation_corner(x, Config, **input_par):
    pos             = np.column_stack((np.arccos(x['cosiota']), np.exp(x['logdistance'])))
    if(not(input_par['injection-approximant']=='Damped-sinusoids') and not(input_par['injection-approximant']=='')):
        expected_values_orientation = [np.arccos(input_par['injection-parameters']['cosiota']), np.exp(input_par['injection-parameters']['logdistance'])]
    else:
        try:
            file = str(Config.get("Plot",'imr-samples'))
            expected_values_orientation = None
            if('GWTC' in file):
                BBH             = h5py.File(file, 'r')['IMRPhenomPv2_posterior']
                IMR_distance    = np.median(BBH['luminosity_distance_Mpc'])
                IMR_inclination = np.median(np.arccos(BBH['costheta_jn']))
                expected_values_orientation = [IMR_inclination, IMR_distance]
                sys.stdout.write(('Using %s to get orientation IMR samples.\n'%(file)))
        except(KeyError,configparser.NoOptionError, configparser.NoSectionError):
            expected_values_orientation = None
    mode_corner(pos,
                labels        = [r'$\iota (rad)$',
                                r'$D(Mpc)$'     ],
                quantiles     = [0.05, 0.5, 0.95],
                show_titles   = True,
                title_kwargs  = {"fontsize": 12},
                use_math_text = True,
                truths        = expected_values_orientation,
                filename      = os.path.join(input_par['output'],'Plots/Parameters/Orientation_corner.png'))

#IMPROVEME: generalize this plot for different amplitudes in case of injections
def amplitudes_corner(x, **input_par):
    params = (np.arccos(x['cosiota']), np.exp(x['logdistance']))
    injected_values = None
    if (input_par['injection-approximant']=='Kerr'):
        injected_values = [np.arccos(input_par['injection-parameters']['cosiota']), np.exp(input_par['injection-parameters']['logdistance'])]
    label_default = [r'$\iota (rad)$', r'$D(Mpc)$']
    for mode in input_par['kerr-modes']:
        s,l,m,n = mode
        if(input_par['amp-non-prec-sym']):
            params = params + (x['A{}{}{}{}'.format(s,l,m,n)],)
            label_default.append('$|A_{%s%d%d%d}|$'%(s,l,m,n))
        else:
            params = params + (x['A{}{}{}{}_1'.format(s,l,m,n)],)+(x['A{}{}{}{}_2'.format(s,l,m,n)],)
            label_default.append('$|A^1_{%s%d%d%d}|$'%(s,l,m,n))
            label_default.append('$|A^2_{%s%d%d%d}|$'%(s,l,m,n))
        if(not(input_par['injection-approximant']=='Damped-sinusoids') and not(input_par['injection-approximant']=='')):
            injected_values.append(np.abs(np.real(input_par['injection-scaling']*(input_par['injection-parameters']['kerr-amplitudes'][(l,m,n)]))))
        pos = np.column_stack(params)
        mode_corner( pos,
                     labels        = label_default,
                     quantiles     = [0.05, 0.5, 0.95],
                     show_titles   = True,
                     title_kwargs  = {"fontsize": 12},
                     use_math_text = True,
                     truths        = injected_values,
                     filename      = os.path.join(input_par['output'], 'Plots/Parameters/Amplitudes_corner.png'))


def f_tau_amp_corner(x, **input_par):
    for pol in input_par['n-ds-modes'].keys():
        for i in range(input_par['n-ds-modes'][pol]):
            pos             = np.column_stack((x['logA_{}_{}'.format(pol,i)],x['f_{}_{}'.format(pol,i)],1e3*x['tau_{}_{}'.format(pol,i)]))
            injected_values = None
            if((i==0) and not(input_par['injection-approximant']=='Damped-sinusoids') and not(input_par['injection-approximant']=='')):
                # Assume that the strongest one is the 220, to predict the other modes, we have the spectroscpy plot.
                injected_values = [None, QNM_fit(2,2,0).f(input_par['injection-parameters']['Mf'],input_par['injection-parameters']['af']), QNM_fit(2,2,0).tau(input_par['injection-parameters']['Mf'],input_par['injection-parameters']['af'])*1e3]
            elif(input_par['injection-approximant']=='Damped-sinusoids'):
                injected_values = [np.log10(input_par['injection-parameters']['A'][pol][i]*input_par['injection-scaling']), input_par['injection-parameters']['f'][pol][i], 1e3*(input_par['injection-parameters']['tau'][pol][i])]
            mode_corner(pos,
                        labels        = [r'$logA_{0}$'.format(i)     ,
                                         r'$f_{0}\,(Hz)$'.format(i)  ,
                                         r'$\tau_{0} (ms)$'.format(i)],
                        quantiles     = [0.05, 0.5, 0.95],
                        show_titles   = True,
                        title_kwargs  = {"fontsize": 12},
                        use_math_text = True,
                        truths        = injected_values,
                        filename      = os.path.join(input_par['output'],'Plots/Parameters/Mode_{}_corner.png'.format(i)))

def tick_function(X): return ['10', '11','12', '13', '14', '15', '16', '17', '18', '19', '20']

def t_start_plot(t0_ds, Mf, **input_par):
    init_plotting()
    Mf                 = Mf * lal.MTSUN_SI
    new_tick_locations = np.array([i*Mf for i in range(10,21)])
    output_dir = os.path.join(input_par['output'], 'Plots')

    if(not(input_par['injection-approximant']=='Damped-sinusoids') and not(input_par['injection-approximant']=='')):
        t0_inj = input_par['injection-parameters']['t0']*1e3
        label_t0_inj = 'Injected value'
    else:
        t0_inj = None
        label_t0_inj = None

    plt.figure(figsize=(6,5))
    ax = plt.subplot(1,1,1)
    ax.hist(t0_ds*1e3, bins=70, histtype='step', color = 'firebrick', lw=1.7)
    plt.axvline(np.mean(t0_ds*1e3), label=r'$\mathrm{Median}$', ls='dotted', c='k', lw=0.9)
    plt.axvline(np.percentile(t0_ds*1e3, 5), label=r'$90\% \mathrm{CI}$', ls='dotted', c='k', lw=0.9)
    plt.axvline(np.percentile(t0_ds*1e3, 95), ls='dotted', c='k', lw=0.9)
    if t0_inj:
        plt.axvline(t0_inj, ls='solid', c='royalblue', lw=0.9, label = label_t0_inj)
    ax.set_xlabel(r'$\mathrm{t_{start} - t_{peak} \, [ms]}$')
    ax.set_ylabel(r'$\mathrm{P(t_{start}|D_{ring})}$')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    ax.grid(False)
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(tick_function(new_tick_locations))
    ax2.set_xlabel(r'$t_{start} - t_{peak}/M_f$', fontsize=10)
    ax2.grid(False)
    plt.xlim(new_tick_locations.min(),new_tick_locations.max())
    plt.grid(False)
    plt.legend()
    plt.savefig(os.path.join(output_dir,'t_start.pdf') ,bbox_inches='tight')

def TEOBPM_intrinsic_corner(x, **input_par):

    pos             = np.column_stack( (x['m1'], x['m2'], x['chi1'], x['chi2'], x['t0']) )
    injected_values = None
    if (input_par['injection-approximant']=='NR'):
        m1   = input_par['injection-parameters']['m1']
        m2   = input_par['injection-parameters']['m2']
        chi1 = input_par['injection-parameters']['s1z']
        chi2 = input_par['injection-parameters']['s2z']
        eta = q/((1+q)*(1+q))
        injected_values = [m1,  m2, chi1, chi2, None]

    mode_corner(  pos,
                  labels        = [r'$m_1 (M_{\odot})$',
                                   r'$m_2 (M_{\odot})$'            ,
                                   r'$\chi_1$'         ,
                                   r'$\chi_2$'         ,
                                   r'$t_{start}$'      ],
                  quantiles     = [0.05, 0.5, 0.95],
                  show_titles   = True,
                  title_kwargs  = {"fontsize": 12},
                  use_math_text = True,
                  truths        = injected_values,
                  filename      = os.path.join(input_par['output'],'Plots/Parameters/TEOBPM_intrinsic_corner.png'))

def Kerr_Newman_intrinsic_corner(x, **input_par):

    pos             = np.column_stack( (x['Mf'], x['af'], x['Q']) )
    injected_values = None
    mode_corner(  pos,
                  labels        = [r'$M_f (M_{\odot})$',
                                   r'$a_f$'            ,
                                   r'$Q$'              ],
                  quantiles     = [0.05, 0.5, 0.95],
                  show_titles   = True,
                  title_kwargs  = {"fontsize": 12},
                  use_math_text = True,
                  truths        = injected_values,
                  filename      = os.path.join(input_par['output'],'Plots/Parameters/Kerr_Newman_intrinsic_corner.png'))

def Mf_af_plot(samples, Mf_LAL_samples, af_LAL_samples, **input_par):
    init_plotting()
    Mf                  = samples['Mf']
    af                  = samples['af']
    logL                = samples['logL']
    if (not(input_par['injection-approximant']=='Damped-sinusoids') and not(input_par['injection-approximant']=='')):
        Mf_inj = input_par['injection-parameters']['Mf']
        af_inj = input_par['injection-parameters']['af']
    samples_stacked = np.column_stack((Mf, af))
    output_dir = os.path.join(input_par['output'], 'Plots')
    plt.figure()
    plt.scatter(Mf, af, c=logL, cmap='Reds',  marker='.', alpha=1.0, label = r'$Ringdown$')
    plot_contour(samples_stacked, [0.95, 0.5])
    if((Mf_LAL_samples is not None) and (af_LAL_samples is not None)):
        samples_stacked_LAL = np.column_stack((Mf_LAL_samples, af_LAL_samples))
        plot_contour(samples_stacked_LAL, [0.95], linest = 'solid', label= 'IMR (LVC)')
    if (not(input_par['injection-approximant']=='Damped-sinusoids') and not(input_par['injection-approximant']=='')):
        plt.axvline(Mf_inj, ls='dashed', c='k', label='Injected values')
        plt.axhline(af_inj, ls='dashed', c='k')
    plt.ylim([0,1])
    plt.grid(alpha=0.2,linestyle='dotted', color='k')
    plt.xlabel(r'$\mathrm{M_f(M_{\odot})}$')
    plt.ylabel(r'$\mathrm{a_f}$')
    plt.savefig(os.path.join(output_dir,'Parameters/Mf_af.pdf') ,bbox_inches='tight')

def omega_tau_eff_plot(x, **kwargs):
    Mf         = x['Mf']
    af         = x['af']
    output_dir = os.path.join(kwargs['output'], 'Plots')
    if ((kwargs['domega-tgr-modes'] is not None) and (kwargs['dtau-tgr-modes'] is None)):
        for mode in kwargs['domega-tgr-modes']:
            (l,m,n)   = mode
            domega    = x['domega_{0}{1}{2}'.format(l, m, n)]
            omega_eff = []
            for i in range(len(Mf)):
                omega_eff.append(QNM_fit(l,m,n).f(Mf[i], af[i])*(1.0+domega[i]))
            pos        = np.column_stack((Mf, af, omega_eff))
            mode_corner(pos,
                        labels        = [r'$M_f \,(M_{\odot})$',
                                         r'$a_f$',
                                         r'$\omega_{%d%d%d} [\!eff] \,(Hz)$'%(l,m,n)],
                        quantiles     = [0.05, 0.5, 0.95],
                        show_titles   = True,
                        title_kwargs  = {"fontsize": 12},
                        use_math_text = True,
                        truths        = None,
                        filename      = os.path.join(kwargs['output'],'Plots/omega_eff_{0}{1}{2}_corner.pdf'.format(l,m,n)))
            pos2        = np.column_stack((Mf, af, domega))
            mode_corner(pos2,
                        labels        = [r'$M_f \,(M_{\odot})$',
                                         r'$a_f$',
                                         r'$\delta \omega_{%d%d%d} \, (Hz)$'%(l,m,n)],
                        quantiles     = [0.05, 0.5, 0.95],
                        show_titles   = True,
                        title_kwargs  = {"fontsize": 12},
                        use_math_text = True,
                        truths        = None,
                        filename      = os.path.join(kwargs['output'],'Plots/domega_corner.pdf'))

    elif ((kwargs['dtau-tgr-modes'] is not None) and (kwargs['domega-tgr-modes'] is None)):
        for mode in kwargs['dtau-tgr-modes']:
            (l,m,n)    = mode
            dtau       = x['dtau_{0}{1}{2}'.format(l, m, n)]
            tau_eff    = []
            for i in range(len(Mf)):
                tau_eff.append(QNM_fit(l,m,n).tau(Mf[i], af[i])*1e3*(1.0+dtau[i]) )
            pos        = np.column_stack((Mf, af, tau_eff))
            output_dir = os.path.join(kwargs['output'], 'Plots')
            mode_corner(pos,
                        labels        = [r'$M_f \,(M_{\odot})$',
                                         r'$a_f$',
                                         r'$\tau_{%d%d%d} [\!eff] (ms)$'%(l,m,n)],
                        quantiles     = [0.05, 0.5, 0.95],
                        show_titles   = True,
                        title_kwargs  = {"fontsize": 12},
                        use_math_text = True,
                        truths        = None,
                        filename      = os.path.join(kwargs['output'],'Plots/tau_eff_{0}{1}{2}_corner.pdf'.format(l,m,n)))
            pos2        = np.column_stack((Mf, af, dtau))
            mode_corner(pos2,
                        labels        = [r'$M_f \,(M_{\odot})$',
                                         r'$a_f$',
                                         r'$\delta \tau_{%d%d%d} \, (Hz)$'%(l,m,n)],
                        quantiles     = [0.05, 0.5, 0.95],
                        show_titles   = True,
                        title_kwargs  = {"fontsize": 12},
                        use_math_text = True,
                        truths        = None,
                        filename      = os.path.join(kwargs['output'],'Plots/dtau_corner.pdf'))
    elif ((kwargs['dtau-tgr-modes'] is not None) and (kwargs['domega-tgr-modes'] is not None)):
        for mode in kwargs['dtau-tgr-modes']:
            (l,m,n)   = mode
            domega    = x['domega_{0}{1}{2}'.format(l, m, n)]
            dtau      = x['dtau_{0}{1}{2}'.format(l, m, n)]
            omega_eff = []
            tau_eff   = []
            for i in range(len(Mf)):
                omega_eff.append(QNM_fit(l,m,n).f(Mf[i], af[i])*(1.0+domega[i]))
                tau_eff.append(QNM_fit(l,m,n).tau(Mf[i], af[i])*1e3*(1.0+dtau[i]) )
            pos        = np.column_stack((Mf, af, omega_eff, tau_eff))
            mode_corner(pos,
                        labels        = [r'$M_f \,(M_{\odot})$',
                                         r'$a_f$',
                                         r'$\omega_{%d%d%d} [\!eff] (Hz)$'%(l,m,n),
                                         r'$\tau_{%d%d%d} [\!eff] (ms)$'%(l,m,n)],
                        quantiles     = [0.05, 0.5, 0.95],
                        show_titles   = True,
                        title_kwargs  = {"fontsize": 12},
                        use_math_text = True,
                        truths        = None,
                        filename      = os.path.join(kwargs['output'],'Plots/omega_tau_eff_{0}{1}{2}_corner.pdf'.format(l,m,n)))
            pos2        = np.column_stack((Mf, af, domega))
            mode_corner(pos2,
                        labels        = [r'$M_f \,(M_{\odot})$',
                                         r'$a_f$',
                                         r'$\delta \omega_{%d%d%d} \, (Hz)$'%(l,m,n)],
                        quantiles     = [0.05, 0.5, 0.95],
                        show_titles   = True,
                        title_kwargs  = {"fontsize": 12},
                        use_math_text = True,
                        truths        = None,
                        filename      = os.path.join(kwargs['output'],'Plots/domega_corner.pdf'))
            pos3        = np.column_stack((Mf, af, dtau))
            mode_corner(pos3,
                        labels        = [r'$M_f \,(M_{\odot})$',
                                         r'$a_f$',
                                         r'$\delta \tau_{%d%d%d} \, (Hz)$'%(l,m,n)],
                        quantiles     = [0.05, 0.5, 0.95],
                        show_titles   = True,
                        title_kwargs  = {"fontsize": 12},
                        use_math_text = True,
                        truths        = None,
                        filename      = os.path.join(kwargs['output'],'Plots/dtau_corner.pdf'))
    else:
        raise Exception("Invalid plotting option in omega-tau effective plot.")

def plot_NR_single_mode(t_geom, hr_geom, hi_geom, **kwargs):

    init_plotting()
    output_dir = os.path.join(kwargs['output'], 'Plots')

    dt_geom                  = np.min(np.diff(t_geom)) # the sampling is NOT uniform
    Amp_geom                 = np.sqrt(hr_geom**2+hi_geom**2)
    Phi_geom                 = np.unwrap(np.angle(hr_geom - 1j*hi_geom))

    t_geom_uniform           = np.arange(t_geom[0], t_geom[-1], dt_geom)
    hr_geom_interp           = np.interp(t_geom_uniform, t_geom, hr_geom)
    hi_geom_interp           = np.interp(t_geom_uniform, t_geom, hi_geom)
    Amp_geom_interp          = np.interp(t_geom_uniform, t_geom, Amp_geom)
    Phi_geom_interp          = np.interp(t_geom_uniform, t_geom, Phi_geom)
    omega_geom_interp        = np.gradient(Phi_geom_interp, dt_geom)
    t_peak_geom_uniform      = t_geom_uniform[np.argmax(Amp_geom_interp)]

    l,m         = kwargs['injection-parameters']['fix-NR-mode'][0]
    M_inj_sec   = kwargs['injection-parameters']['M']*lal.MTSUN_SI
    t_phys      = t_geom_uniform*M_inj_sec
    freq_phys   = (omega_geom_interp/(2.*np.pi)) * (M_inj_sec)**(-1)
    t_peak_phys = t_phys[np.argmax(Amp_geom_interp)]

    new_tick_locations = np.array([t_peak_phys+10*i*kwargs['injection-parameters']['Mf']*lal.MTSUN_SI for i in range(0,9)])

    f = plt.figure(figsize=(12,8))
    ax = plt.subplot(2,2,1)
    ax.plot(t_phys, hr_geom_interp, c='firebrick', label=r'$\mathrm{h_r}$')
    ax.axvline(t_peak_phys, ls='dotted', c='k')
    ax.set_xlim([t_peak_phys-50*M_inj_sec, t_peak_phys+130*M_inj_sec])
    ax.legend(loc='best')
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(tick_function(new_tick_locations))
    ax2.set_xlabel(r'$t_{start} - t_{peak}/M_f$', fontsize=10)
    ax = plt.subplot(2,2,3)
    ax.plot(t_phys, hi_geom_interp, c='firebrick', label=r'$\mathrm{h_i}$')
    ax.axvline(t_peak_phys, ls='dotted', c='k')
    ax.set_xlim([t_peak_phys-50*M_inj_sec, t_peak_phys+130*M_inj_sec])
    ax.legend(loc='best')
    plt.xlabel('Time (s)')
    ax = plt.subplot(2,2,2)
    ax.plot(t_phys, freq_phys, c='firebrick', label=r'$\mathrm{Freq}$')
    ax.axhline(kwargs['injection-parameters']['f_220'], ls='dotted', c='k', alpha=0.8, label=r'$\mathrm{f_{220}}$' )
    ax.axhline(kwargs['injection-parameters']['f_220_peak'], ls='dashed', c='darkgreen', alpha=0.8, label=r'$\mathrm{f^{peak}_{22}}$')
    ax.axvline(t_peak_phys, ls='dotted', c='k')
    ax.set_ylim([100, kwargs['injection-parameters']['f_220']+150])
    ax.set_xlim([t_peak_phys-50*M_inj_sec, t_peak_phys+130*M_inj_sec])
    ax.legend(loc='upper left')
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(tick_function(new_tick_locations))
    ax2.set_xlabel(r'$t_{start} - t_{peak}/M_f$', fontsize=10)
    ax = plt.subplot(2,2,4)
    ax.plot(t_phys, Amp_geom_interp, c='firebrick', label=r'$\mathrm{Amp}$')
    ax.axvline(t_peak_phys, ls='dotted', c='k', label=r'$\mathrm{t^{peak}_{22}}$')
    ax.set_xlim([t_peak_phys-50*M_inj_sec, t_peak_phys+130*M_inj_sec])
    ax.legend(loc='upper right')
    plt.xlabel('Time (s)')
    plt.suptitle('SXS:BBH:{0}'.format(kwargs['injection-parameters']['SXS-ID']), size=24)
    plt.tight_layout(rect=[0,0,1,0.95])
    f.subplots_adjust(hspace=0)
    plt.savefig(os.path.join(output_dir,'SXS_{0}_N_{1}_l_{2}_m_{3}.pdf'.format(kwargs['injection-parameters']['SXS-ID'], kwargs['injection-parameters']['N'], l, m)), bbox_inches='tight')

def single_time_delay_plots(dt_vec, **input_par):
    for det in input_par['detectors']:
        if(det==input_par['ref-det']):
            pass
        else:
            plt.figure()
            plt.hist(dt_vec[det], bins=50, alpha=0.8)
            plt.xlabel(r'$\Delta t_{%s-%s}$ (s)'%(input_par['ref-det'], det))
            plt.savefig(os.path.join(input_par['output'],'Plots/Parameters/dt_%s%s_posterior.png'%(input_par['ref-det'], det)))
            plt.figure()
            plt.plot(dt_vec[det],'.')
            plt.xlabel(r'$\Delta t_{%s-%s}$ (s)'%(input_par['ref-det'], det))
            plt.xlabel(r'$N_{samples}$')
            plt.savefig(os.path.join(input_par['output'],'Plots/Parameters/dt_%s%s_chain.png'%(input_par['ref-det'], det)))

def sky_location_plots(x, Config, **input_par):

    dt_vec       = {}
    ra_vec       = []
    dec_vec      = []
    tg_vec       = []
    non_ref_dets = []
    ref_det      = input_par['ref-det']
    sky_frame    = input_par['sky-frame']

    for det in input_par['detectors']:
        if(det==ref_det):
            pass
        else:
            non_ref_dets.append(det)
    if(input_par['template']=='Damped-sinusoids'):
        sky_loc_header = 'ra\tdec\ttg'
    else:
        sky_loc_header = 'ra\tdec\ttg\tdist'
    for det in non_ref_dets:
        sky_loc_header = sky_loc_header + '\tdt_'+ ref_det + det
        dt_vec[det]    = []

    for par in x:
        if(sky_frame == 'detector'):
            tg, ra, dec = DetFrameToEquatorial(lal.cached_detector_by_prefix[ref_det],
                                               lal.cached_detector_by_prefix[input_par['nonref-det']],
                                               input_par['trigtime'],
                                               np.arccos(par['cos_altitude']),
                                               par['azimuth'])
        elif(sky_frame == 'equatorial'):
            tg, ra, dec  = 0.0, par['ra'], par['dec']
        ra_vec.append(ra)
        dec_vec.append(dec)
        tg_vec.append(tg)
        for d in non_ref_dets:
            dt_vec[d].append(lal.ArrivalTimeDiff(lal.cached_detector_by_prefix[d].location,
                                                 lal.cached_detector_by_prefix[ref_det].location,
                                                 ra,
                                                 dec,
                                                 lal.LIGOTimeGPS(float(input_par['trigtime']))))
    if(len(input_par['detectors']) > 1):
        dt_tuple = np.array([dt_vec[det] for det in non_ref_dets])
        if(input_par['template']=='Damped-sinusoids'):
            np.savetxt(os.path.join(input_par['output'],'Nested_sampler/Sky-loc-samples.txt'), np.column_stack((np.array(ra_vec), np.array(dec_vec), np.array(tg_vec), dt_tuple.transpose())), header=sky_loc_header)
        else:
            np.savetxt(os.path.join(input_par['output'],'Nested_sampler/Sky-loc-samples.txt'), np.column_stack((np.array(ra_vec), np.array(dec_vec), np.array(tg_vec), np.array(np.exp(x['logdistance'])), dt_tuple.transpose())), header=sky_loc_header)
        single_time_delay_plots(dt_vec, **input_par)
    else:
        if(input_par['template']=='Damped-sinusoids'):
            np.savetxt(os.path.join(input_par['output'],'Nested_sampler/Sky-loc-samples.txt'), np.column_stack((np.array(ra_vec), np.array(dec_vec), np.array(tg_vec))), header=sky_loc_header)
        else:
            np.savetxt(os.path.join(input_par['output'],'Nested_sampler/Sky-loc-samples.txt'), np.column_stack((np.array(ra_vec), np.array(dec_vec), np.array(tg_vec), np.array(np.exp(x['logdistance'])))), header=sky_loc_header)

    if not(input_par['injection-approximant']==''):
        if(sky_frame == 'detector'):
            inj_tg, inj_ra, inj_dec = DetFrameToEquatorial(lal.cached_detector_by_prefix[ref_det], lal.cached_detector_by_prefix[input_par['nonref-det']], input_par['trigtime'], np.arccos(input_par['injection-parameters']['cos_altitude']), input_par['injection-parameters']['azimuth'])
        elif(sky_frame == 'equatorial'):
            inj_ra  = input_par['injection-parameters']['ra']
            inj_dec = input_par['injection-parameters']['dec']

        inj_psi = input_par['injection-parameters']['psi']
        inj_time_delay = {'{}_'.format(ref_det)+d2: lal.ArrivalTimeDiff(lal.cached_detector_by_prefix[d2].location,lal.cached_detector_by_prefix['{}'.format(ref_det)].location,inj_ra,inj_dec,lal.LIGOTimeGPS(float(input_par['trigtime']))) for d2 in non_ref_dets}
        expected_values_skypos = [inj_ra, inj_dec, inj_psi ] + [inj_time_delay['{}_{}'.format(ref_det, det)] for det in non_ref_dets]
    else:
        try:
            file = str(Config.get("Plot",'imr-samples'))
            expected_values_skypos = None
            if('GWTC' in file):
                BBH     = h5py.File(file, 'r')['IMRPhenomPv2_posterior']
                IMR_ra  = np.median(BBH['right_ascension'])
                IMR_dec = np.median(BBH['declination'])
                IMR_time_delay = {'{}_'.format(ref_det)+d2: lal.ArrivalTimeDiff(lal.cached_detector_by_prefix[d2].location,lal.cached_detector_by_prefix['{0}'.format(ref_det)].location,IMR_ra,IMR_dec,lal.LIGOTimeGPS(float(input_par['trigtime']))) for d2 in non_ref_dets}
                expected_values_skypos = [IMR_ra, IMR_dec, None] + [IMR_time_delay['{}_{}'.format(ref_det, det)] for det in non_ref_dets]
                sys.stdout.write(('Using %s to get sky position IMR samples.'%(file)))
        except(KeyError,configparser.NoOptionError, configparser.NoSectionError):
            expected_values_skypos = None
    #IMPROVEME: produce the plot properly also when parameters are fixed
    try:
        if(len(input_par['detectors']) > 1):
            mode_corner(np.column_stack((np.array(ra_vec), np.array(dec_vec), np.array(x['psi']), dt_tuple.transpose())),
                    labels        = [r'$ra$', r'$dec$', r'$psi$'] + [r'$\Delta t_{%s-%s}$ (s)'%(ref_det, det) for det in non_ref_dets],
                    quantiles     = [0.05, 0.5, 0.95],
                    show_titles   = True,
                    title_kwargs  = {"fontsize": 12},
                    use_math_text = True,
                    truths        = expected_values_skypos,
                    filename      = os.path.join(input_par['output'],'Plots/Parameters/corner_skypos.png'))
        else:
            mode_corner(np.column_stack((np.array(ra_vec), np.array(dec_vec), np.array(x['psi']))),
                    labels        = [r'$ra$', r'$dec$', r'$psi$'],
                    quantiles     = [0.05, 0.5, 0.95],
                    show_titles   = True,
                    title_kwargs  = {"fontsize": 12},
                    use_math_text = True,
                    truths        = expected_values_skypos,
                    filename      = os.path.join(input_par['output'],'Plots/Parameters/corner_skypos.png'))
    except(ValueError):
        pass

def read_Mf_af_IMR_posterior(Config, **input_par):

    # Get GR prediction (IMR + UIB NR fits applied on real data) to plot expected values. Using non-precessing fits since no phi12 angle was released alongside GWTC-1
    # IMPROVEME: GWTC-1 did not release spin angles, so precessing fits cannot be applited on this set of samples. When GWTC-2 is out, apply precessing fits.
    try:
        file = str(Config.get("Plot",'imr-samples'))
        if('GWTC' in file):
            BBH   = h5py.File(file, 'r')['IMRPhenomPv2_posterior']
            m1_samples    = BBH['m1_detector_frame_Msun']
            m2_samples    = BBH['m2_detector_frame_Msun']
            chi1_samples  = BBH['spin1']
            chi2_samples  = BBH['spin2']
            tilt1_samples = np.arccos(BBH['costilt1'])
            tilt2_samples = np.arccos(BBH['costilt2'])
            Mf_d          = []
            af_d          = []
            for (m1, m2, chi1, chi2, tilt1, tilt2) in zip(m1_samples, m2_samples, chi1_samples, chi2_samples, tilt1_samples, tilt2_samples):
                af_x = bbh_final_spin_projected_spins(m1, m2, chi1, chi2, tilt1, tilt2, 'UIB2016', truncate = bbh_Kerr_trunc_opts.trunc)
                af_d.append(af_x)
                Mf_d.append(bbh_final_mass_projected_spins(m1, m2, chi1, chi2, tilt1, tilt2, 'UIB2016'))
            Mf_d = np.array(Mf_d)
            af_d = np.array(Mf_d)
        else:
            package_datapath = import_datafile_path(file)
            PYRING_PREFIX    = set_prefix(warning_message=False)
            custom_datapath  = os.path.join(PYRING_PREFIX, file)
            if(os.path.exists(package_datapath)):
                print('* Fetching the IMR posterior from the default ones included in the package.\n')
                file = package_datapath
            elif(os.path.exists(custom_datapath)):
                print('* Fetching the IMR posterior relatively to the PYRING_PREFIX.\n')
                file = custom_datapath
            else:
                print('* Fetching the IMR posterior using the provided absolute path.\n')
                pass
            Mf_d = np.genfromtxt(file, names=True)['Mf']
            af_d = np.genfromtxt(file, names=True)['af']
        Mf  = np.median(Mf_d)
        dMf = np.std(Mf_d, ddof=1)
        af  = np.median(af_d)
        daf = np.std(af_d, ddof=1)

    except (KeyError,configparser.NoOptionError, configparser.NoSectionError, OSError):
        try:
            if(not(input_par['injection-approximant']=='Damped-sinusoids') and not(input_par['injection-approximant']=='')):
                Mf   = input_par['injection-parameters']['Mf']
                dMf  = (5./100.)*Mf #IMPROVEME: substitute with an estimate of NR uncertainty
                Mf_d = np.random.normal(Mf, dMf/2, 1000)
                af   = input_par['injection-parameters']['af']
                daf  = (2./100.)*af #IMPROVEME: substitute with an estimate of NR uncertainty
                af_d = np.random.normal(af, daf/2, 1000)
            else:
                Mf   = Config.getfloat("Priors",'mf-time-prior')
                dMf  = Config.getfloat("Plot",'dmf')#Estimate of half the 95% CI, which is 2sigma
                Mf_d = np.random.normal(Mf, dMf/2, 1000)
                af   = Config.getfloat("Plot",'af')
                daf  = Config.getfloat("Plot",'daf')#Estimate of half the 95% CI, which is 2sigma
                af_d = np.random.normal(af, daf/2, 1000)
        except (KeyError,configparser.NoOptionError, configparser.NoSectionError):
            sys.stdout.write('No IMR posterior was passed.\n')
            Mf_d = None
            af_d = None
    if((Mf_d is not None) and (af_d is not None)):
        sys.stdout.write('* To predict the GR spectrum of QNM or final mass and spin, the following parameters will be used:\n\n  Mf: {:.3f}  ({:.3f})\n  af: {:.3f}   ({:.3f})\n\n'.format(Mf, dMf, af, daf))
    return Mf_d, af_d

def plot_ACF(time, acf, label, output_path):

    init_plotting()
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.plot(time, acf, linewidth=0.5, color = 'k', label=r'{}'.format(label))
    ax.set_xlabel(r'$\tau\,(s)$', fontsize=18)
    ax.set_ylabel(r'$C(\tau)$'  , fontsize=18)
    ax.legend()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close('all')

def plot_PSD(freqs, psd, label, output_path):

    init_plotting()
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.loglog(freqs, psd, linewidth=0.5, color = 'k', label=r'{}'.format(label))
    ax.set_xlabel(r'$f\,(Hz)$',         fontsize=18)
    ax.set_ylabel(r'$S(f)\,(Hz^{-1})$', fontsize=18)
    ax.legend()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close('all')

def plot_ACF_compare(time1, acf1, label1, time2, acf2, label2, output_path):

    init_plotting()
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.plot(time1, acf1, linewidth=0.5, color = 'k',         label=r'{}'.format(label1), linestyle='dotted')
    ax.plot(time2, acf2, linewidth=0.5, color = 'firebrick', label=r'{}'.format(label2), alpha=0.8)
    ax.set_xlabel(r'$\tau\,(s)$', fontsize=18)
    ax.set_ylabel(r'$C(\tau)$'  , fontsize=18)
    ax.legend()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close('all')

def plot_PSD_compare(freqs1, psd1, label1, freqs2, psd2, label2, output_path):

    init_plotting()
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    ax.loglog(freqs1, psd1, linewidth=0.5, color = 'firebrick', label=r'{}'.format(label1), alpha=0.8)
    ax.loglog(freqs2, psd2, linewidth=0.5, color = 'k',         label=r'{}'.format(label2), linestyle='dotted')
    ax.set_xlabel(r'$f\,(Hz)$',        fontsize=18)
    ax.set_ylabel(r'$S(f)\,(Hz^{-1})$',fontsize=18)
    ax.legend()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close('all')

def UNUSED_noise_evidence_density(t0_samples,noise_model):
    logZnoise = []
    time = noise_model.times-noise_model.tevent
    for t0 in t0_samples:
        index = np.abs(t0-time).argmin()
        logZnoise.append(np.sum([- 0.5*np.einsum('i, ij, j',s[index:],Cinv[index:,index:],s[index:]) for s,Cinv in zip(noise_model.data,noise_model.inverse_covariance)]))
    return np.array(logZnoise)
