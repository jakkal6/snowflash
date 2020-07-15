import numpy as np
import os
import pandas as pd


def analysis(a, m, output, detector, channel_groups, tot_file):
    """Does analysis on snowglobes output and writes out to ascii files in output \n
        Kinda a mess since it's hacked in from historical scripts \n
        Currently calculating mean energy and total counts for each detector channel \n
        for each timestep and calculating time-integrated mean energies \n
        Input: alpha, mass, for snowglobes code [s], \n
        output directory path, detector configuration\n
        nomix_tot file for time-integrated quantities \n
        Output: None"""
    channels = get_all_channels(channel_groups)

    time_filepath = os.path.join('./fluxes/', f'pinched_a{a}_m{m}_key.dat')
    time = np.loadtxt(time_filepath, skiprows=1, usecols=[1], unpack=True)
    n_time = len(time)

    energy_bins = load_energy_bins(channel=channels[0], i=1,
                                   a=a, m=m, detector=detector)
    n_bins = len(energy_bins)

    integrated_counts = {'Total': np.zeros(n_bins)}
    time_totals = {'Total': np.zeros(n_time)}
    time_avg = {'Total': np.zeros(n_time)}

    for group in channel_groups:
        integrated_counts[group] = np.zeros(n_bins)
        time_totals[group] = np.zeros(n_time)
        time_avg[group] = np.zeros(n_time)

    for i in range(1, n_time + 1):
        channel_counts = load_channel_counts(channels=channels,
                                             i=i, a=a, m=m,
                                             detector=detector)

        group_counts = get_group_counts(channel_counts,
                                        groups=channel_groups,
                                        n_bins=n_bins)

        for group in integrated_counts:
            integrated_counts[group] += group_counts[group]

        group_totals = get_totals(group_counts)

        group_avg = get_avg(group_counts=group_counts,
                            group_totals=group_totals,
                            energy_bins=energy_bins)

        for group in group_totals:
            time_totals[group][i-1] = group_totals[group]
            time_avg[group][i-1] = group_avg[group]

    time_table = create_time_table(timesteps=time,
                                   time_totals=time_totals,
                                   time_avg=time_avg)

    save_time_table(table=time_table, detector=detector,
                    a=a, m=m, output=output)

    # TODO: write integrated row

    integrated_totals = get_totals(integrated_counts)
    integrated_avg = get_avg(group_counts=integrated_counts,
                             group_totals=integrated_totals,
                             energy_bins=energy_bins)

    # nomix_tot.write(str(m)+"\t"+str(nomix_avg_tot)+"\t"+str(nomix_avg_ibd)+"\t"+str(nomix_avg_es)+"\t"+str(nomix_avg_eo16)+"\t"+str(nomix_avg_ao16)+"\t"+str(nomix_avg_nc)+"\n")
    # return time_avg, time_totals, integrated_avg, integrated_totals


# ===========================================================
#                   Raw channel counts
# ===========================================================
def get_all_channels(groups):
    """Extract list of channels from dict of channel groups
    """
    channels = []
    for group, subs in groups.items():
        channels += subs

    return channels


def load_channel_counts(channels, i, a, m, detector):
    """Load all raw channel counts into dict
    """
    channel_counts = {}  # arrays of channel counts per energy bin
    for chan in channels:
        channel_counts[chan] = load_channel_dat(channel=chan, i=i, a=a,
                                                m=m, detector=detector)
    return channel_counts


def load_channel_dat(channel, i, a, m, detector):
    """Load array of detection counts per energy bin
    """
    filepath = channel_dat_filepath(channel=channel, i=i, a=a, m=m, detector=detector)
    return np.genfromtxt(filepath, skip_footer=2, usecols=[1], unpack=True)


def channel_dat_filepath(channel, i, a, m, detector):
    """Return filepath to snowglobes output file
    """
    return f'./out/pinched_a{a}_m{m}_{i}_{channel}_{detector}_events_smeared.dat'


def load_energy_bins(channel, i, a, m, detector):
    """Load array of energy bins (MeV) from a snowglobes output file
    """
    filepath = channel_dat_filepath(channel=channel, i=i, a=a, m=m, detector=detector)
    energy_bins = np.genfromtxt(filepath, skip_footer=2, usecols=[0], unpack=True)
    return energy_bins * 1000


# ===========================================================
#                   Group counts/averages
# ===========================================================
def get_group_counts(channel_counts, groups, n_bins):
    """Sum channel counts by group
    """
    group_counts = {'Total': np.zeros(n_bins)}

    for group, sub_channels in groups.items():
        counts = np.zeros(n_bins)

        for chan in sub_channels:
            counts += channel_counts[chan]

        group_counts['Total'] += counts
        group_counts[group] = counts

    return group_counts


def get_totals(group_counts):
    """Get total counts over all energy bins
    """
    totals = {}
    for group in group_counts:
        totals[group] = np.sum(group_counts[group])

    return totals


def get_avg(group_counts, group_totals, energy_bins):
    """Get group average energies
    """
    group_avg = {}

    for group, total in group_totals.items():
        if total != 0:
            avg = np.sum(group_counts[group] * energy_bins) / total
        else:
            avg = 0

        group_avg[group] = avg

    return group_avg


# ===========================================================
#                   Time-dependent data
# ===========================================================
def create_time_table(timesteps, time_totals, time_avg):
    """Construct a DataFrame from time-dependent arrays of mean energies/total counts
    """
    table = pd.DataFrame()
    table['Time'] = timesteps

    for group in time_avg:
        table[f'Avg_{group}'] = time_avg[group]

    for group in time_totals:
        table[f'Tot_{group}'] = time_totals[group]

    return table


def save_time_table(table, detector, a, m, output):
    """Save time-dependent table to file
    """
    filepath = os.path.join(output, f"{detector}_analysis_a{a}_m{m}.dat")
    string = table.to_string(index=False, justify='left')

    with open(filepath, 'w') as f:
        f.write(string)
