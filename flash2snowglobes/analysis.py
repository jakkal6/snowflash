import numpy as np
import os
import pandas as pd


def analyze_output(tab,
                   mass,
                   output,
                   detector,
                   channel_groups):
    """Analyze snowglobes output and writes to ascii files

    Currently calculating mean energy and total counts for each detector channel
    for each timestep and calculating time-integrated mean energies

    parameters
    ----------
    tab : int
    mass : float or int
    output : str
    detector : str
    channel_groups : {}
    """
    channels = get_all_channels(channel_groups)

    time_filepath = os.path.join('./fluxes/', f'pinched_tab{tab}_m{mass}_key.dat')
    time = np.loadtxt(time_filepath, skiprows=1, usecols=[1], unpack=True)
    n_time = len(time)

    energy_bins = load_energy_bins(channel=channels[0],
                                   i=1,
                                   tab=tab,
                                   mass=mass,
                                   detector=detector)
    n_bins = len(energy_bins)

    time_totals = {'total': np.zeros(n_time)}
    time_avg = {'total': np.zeros(n_time)}

    for group in channel_groups:
        time_totals[group] = np.zeros(n_time)
        time_avg[group] = np.zeros(n_time)

    for i in range(n_time):
        channel_counts = load_channel_counts(channels=channels,
                                             i=i + 1,
                                             tab=tab,
                                             mass=mass,
                                             detector=detector)

        group_counts = get_group_counts(channel_counts,
                                        groups=channel_groups,
                                        n_bins=n_bins)

        group_totals = get_totals(group_counts)
        group_avg = get_avg(group_counts=group_counts,
                            group_totals=group_totals,
                            energy_bins=energy_bins)

        for group in group_totals:
            time_totals[group][i] = group_totals[group]
            time_avg[group][i] = group_avg[group]

    timebin_table = create_timebin_table(timesteps=time,
                                         time_totals=time_totals,
                                         time_avg=time_avg)

    save_timebin_table(table=timebin_table,
                       detector=detector,
                       tab=tab,
                       mass=mass,
                       output=output)


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


def load_channel_counts(channels, i, tab, mass, detector):
    """Load all raw channel counts into dict
    """
    channel_counts = {}  # arrays of channel counts per energy bin
    for chan in channels:
        channel_counts[chan] = load_channel_dat(channel=chan, i=i, tab=tab,
                                                mass=mass, detector=detector)
    return channel_counts


def load_channel_dat(channel, i, tab, mass, detector):
    """Load array of detection counts per energy bin
    """
    filepath = channel_dat_filepath(channel=channel, i=i, tab=tab, mass=mass, detector=detector)
    return np.genfromtxt(filepath, skip_footer=2, usecols=[1], unpack=True)


def channel_dat_filepath(channel, i, tab, mass, detector):
    """Return filepath to snowglobes output file
    """
    return f'./out/pinched_tab{tab}_m{mass}_{i}_{channel}_{detector}_events_smeared.dat'


def load_energy_bins(channel, i, tab, mass, detector):
    """Load array of energy bins (MeV) from a snowglobes output file
    """
    filepath = channel_dat_filepath(channel=channel, i=i, tab=tab, mass=mass, detector=detector)
    energy_bins = np.genfromtxt(filepath, skip_footer=2, usecols=[0], unpack=True)
    return energy_bins * 1000


# ===========================================================
#                   Group counts/averages
# ===========================================================
def get_group_counts(channel_counts, groups, n_bins):
    """Sum channel counts by group
    """
    group_counts = {'total': np.zeros(n_bins)}

    for group, sub_channels in groups.items():
        counts = np.zeros(n_bins)

        for chan in sub_channels:
            counts += channel_counts[chan]

        group_counts['total'] += counts
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
#                   Timebinned data
# ===========================================================
def create_timebin_table(timesteps, time_totals, time_avg):
    """Construct a DataFrame from timebinned arrays of mean energies/total counts
    """
    table = pd.DataFrame()
    table['time'] = timesteps

    for group in time_avg:
        table[f'energy_{group}'] = time_avg[group]

    for group in time_totals:
        table[f'counts_{group}'] = time_totals[group]

    return table


def save_timebin_table(table, detector, tab, mass, output):
    """Save timebinned table to file
    """
    mset = {1: 'LMP', 2: 'LMP+N50', 3: 'SNA'}[tab]
    filepath = os.path.join(output, f"{detector}_analysis_{mset}_m{mass}.dat")
    string = table.to_string(index=False, justify='left')

    with open(filepath, 'w') as f:
        f.write(string)
