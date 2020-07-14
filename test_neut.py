import numpy as np
import os

def analysis(a,m,output,detector,nomix_tot):
        """Does analysis on snowglobes output and writes out to ascii files in output \n
        Kinda a mess since it's hacked in from historical scripts \n
        Currently calculating mean energy and total counts for each detector channel \n
        for each timestep and calculating time-integrated mean energies \n
        Input: alpha, mass, for snowglobes code [s], \n
        output directory path, detector configuration\n
        nomix_tot file for time-integrated quantities \n
        Output: None"""

        groups = {'IBD': ['ibd'],
                  'ES': ['nue_e'],
                  'nu_e_O16': ['nue_O16'],
                  'anu_e_O16': ['nuebar_O16'],
                  'NC': ['nc_nue_O16', 'nc_nuebar_O16',
                         'nc_numu_O16', 'nc_numubar_O16',
                         'nc_nutau_O16', 'nc_nutaubar_O16']
                  }
        channels = get_all_channels(groups)

        time_filepath = os.path.join('./fluxes/', f'pinched_a{a}_m{m}_key.dat')
        time = np.loadtxt(time_filepath, skiprows=1, usecols=[1], unpack=True)
        n_time = len(time)

        energy_bins = load_energy_bins(channel=channels[0], i=1,
                                       a=a, m=m, detector=detector)
        n_bins = len(energy_bins)

        integrated_counts = {}  # total time-integrated group counts
        for group in groups:
            integrated_counts[group] = np.zeros(n_bins)

        # TODO: create empty time-arrays

        for i in range(1, n_time+1):
            # arrays of channel counts per energy bin
            channel_counts = load_channel_counts(channels, i=i, a=a, m=m, detector=detector)

            # arrays of group counts per energy bin
            group_counts = get_group_counts(channel_counts, groups=groups, n_bins=n_bins)

            # add to time-integrated counts
            for group in integrated_counts:
                integrated_counts[group] += group_counts[group]

            # total group counts over all energy bins
            group_totals = get_totals(group_counts)

            # average energy over all energy_bins
            group_avg = get_avg(group_counts, group_totals=group_totals,
                                energy_bins=energy_bins)

            # TODO: insert totals, avg to time arrays

        # TODO:
        #  - put time-arrays into dataframe
        #  - save dataframe
        integrated_totals = get_totals(integrated_counts)
        integrated_avg = get_avg(group_counts=integrated_counts,
                                 group_totals=integrated_totals,
                                 energy_bins=energy_bins)

        return integrated_avg, integrated_totals

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


def get_group_counts(channel_counts, groups, n_bins):
    """Sum channel counts by group
    """
    group_counts = {}
    for group, sub_channels in groups.items():
        group_counts[group] = np.zeros(n_bins)

        for chan in sub_channels:
            group_counts[group] += channel_counts[chan]

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


def load_channel_dat(channel, i, a, m, detector):
    """Load array of detection counts per energy bin
    """
    filepath = channel_dat_filepath(channel=channel, i=i, a=a, m=m, detector=detector)
    return np.genfromtxt(filepath, skip_footer=2, usecols=[1], unpack=True)


def load_energy_bins(channel, i, a, m, detector):
    """Load array of energy bins (MeV) from a snowglobes output file
    """
    filepath = channel_dat_filepath(channel=channel, i=i, a=a, m=m, detector=detector)
    energy_bins = np.genfromtxt(filepath, skip_footer=2, usecols=[0], unpack=True)
    return energy_bins * 1000


def channel_dat_filepath(channel, i, a, m, detector):
    """Return filepath to snowglobes output file
    """
    return f'./out/pinched_a{a}_m{m}_{i}_{channel}_{detector}_events_smeared.dat'
