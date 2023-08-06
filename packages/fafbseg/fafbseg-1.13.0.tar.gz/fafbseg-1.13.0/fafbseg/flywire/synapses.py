#    A collection of tools to interface with manually traced and autosegmented
#    data in FAFB.
#
#    Copyright (C) 2019 Philipp Schlegel
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

import navis

import datetime as dt
import numpy as np
import pandas as pd

from functools import partial
from pathlib import Path
from tqdm.auto import trange

from .segmentation import is_latest_root
from .utils import parse_root_ids, get_cave_client, retry, get_synapse_areas

from ..utils import make_iterable
from ..synapses.utils import catmaid_table
from ..synapses.transmitters import collapse_nt_predictions

__all__ = ['fetch_synapses', 'fetch_connectivity', 'predict_transmitter',
           'fetch_adjacency', 'synapse_counts']


def split_axon_dendrite(x):
    pass


def synapse_counts(x, by_neuropil=False, min_score=30, live_query=False,
                   batch_size=10, dataset='production', **kwargs):
    """Fetch synapse counts for given root IDs.

    Parameters
    ----------
    x :             int | list of int | Neuron/List
                    Either a FlyWire segment ID (i.e. root ID), a list thereof or
                    a Neuron/List. For neurons, the ``.id`` is assumed to be the
                    root ID. If you have a neuron (in FlyWire space) but don't
                    know its ID, use :func:`fafbseg.flywire.neuron_to_segments`
                    first.
    by_neuropil :   bool
                    If True, returned DataFrame will contain a break down by
                    neuropil.
    min_score :     int, optional
                    Minimum "cleft score". The default of 30 is what Buhmann et al.
                    used in the paper.
    live_query :    bool
                    Whether to query against the live data or against the latest
                    materialized table. The latter is useful if you are working
                    with IDs that you got from another annotation table.
    batch_size :    int
                    Number of IDs to query per batch. Too large batches might
                    lead to truncated tables: currently individual queries can
                    not return more than 200_000 rows and you will see a warning
                    if that limit is exceeded.
    dataset :       str | CloudVolume
                    Against which FlyWire dataset to query::
                        - "production" (current production dataset, fly_v31)
                        - "sandbox" (i.e. fly_v26)
    **kwargs
                    Keyword arguments are passed through to
                    :func:`fafbseg.flywire.fetch_synapses`.

    Returns
    -------
    pandas.DataFrame
                    If ``by_neuropil=False`` returns counts indexed by root ID.
                    If ``by_neuropil=True`` returns counts indexed by root ID
                    and neuropil.

    """
    # Parse root IDs
    ids = parse_root_ids(x)

    # First get the synapses
    syn = fetch_synapses(x, pre=True, post=True, attach=False,
                         min_score=min_score,
                         transmitters=True, live_query=live_query,
                         neuropils=by_neuropil,
                         batch_size=batch_size,
                         dataset=dataset, **kwargs)

    pre = syn[syn.pre.isin(x)]
    post = syn[syn.post.isin(x)]

    if not by_neuropil:
        counts = pd.DataFrame()
        counts['id'] = ids
        counts['pre'] = pre.value_counts('pre').reindex(ids).fillna(0).values
        counts['post'] = post.value_counts('post').reindex(ids).fillna(0).values
        counts.set_index('id', inplace=True)
    else:
        pre_grp = pre.groupby(['pre', 'neuropil']).size()
        pre_grp = pre_grp[pre_grp > 0]
        pre_grp.index.set_names(['id', 'neuropil'], inplace=True)

        post_grp = post.groupby(['post', 'neuropil']).size()
        post_grp = post_grp[post_grp > 0]
        post_grp.index.set_names(['id', 'neuropil'], inplace=True)

        neuropils = np.unique(np.append(pre_grp.index.get_level_values(1),
                                        post_grp.index.get_level_values(1)))

        index = pd.MultiIndex.from_product([ids, neuropils],
                                           names=['id', 'neuropil'])

        counts = pd.concat([pre_grp.reindex(index).fillna(0),
                            post_grp.reindex(index).fillna(0)],
                           axis=1)
        counts.columns = ['pre', 'post']
        counts = counts[counts.max(axis=1) > 0]

    return counts


def predict_transmitter(x, single_pred=False, weighted=True, live_query=True,
                        neuropils=None, batch_size=10, dataset='production', **kwargs):
    """Fetch neurotransmitter predictions for neurons.

    Based on Eckstein et al. (2020). The per-synapse predictions are collapsed
    into per-neuron prediction by calculating the average confidence for
    each neurotransmitter across all synapses weighted by the "cleft score".
    Bottom line: higher confidence synapses have more weight than low confidence
    synapses.

    Parameters
    ----------
    x :             int | list of int | Neuron/List
                    Either a FlyWire segment ID (i.e. root ID), a list thereof or
                    a Neuron/List. For neurons, the ``.id`` is assumed to be the
                    root ID. If you have a neuron (in FlyWire space) but don't
                    know its ID, use :func:`fafbseg.flywire.neuron_to_segments`
                    first.
    single_pred :   bool
                    Whether to only return the highest probability transmitter
                    for each neuron.
    weighted :      bool
                    If True, will weight predictions based on confidence: higher
                    cleft score = more weight.
    live_query :    bool
                    Whether to query against the live data or against the latest
                    materialized table. The latter is useful if you are working
                    with IDs that you got from another annotation table.
    neuropils :     str | list of str, optional
                    Provide neuropil (e.g. ``'AL_R'``) or list thereof (e.g.
                    ``['AL_R', 'AL_L']``) to filter predictions to these ROIs.
                    Prefix neuropil with a tilde (e.g. ``~AL_R``) to exclude it.
    batch_size :    int
                    Number of IDs to query per batch. Too large batches might
                    lead to truncated tables: currently individual queries can
                    not return more than 200_000 rows and you will see a warning
                    if that limit is exceeded.
    dataset :       str | CloudVolume
                    Against which FlyWire dataset to query::
                        - "production" (current production dataset, fly_v31)
                        - "sandbox" (i.e. fly_v26)
    **kwargs
                    Keyword arguments are passed through to
                    :func:`fafbseg.flywire.fetch_synapses`.


    Returns
    -------
    pandas.DataFrame
                    If `single_pred=False`: returns a dataframe with all
                    per-transmitter confidences for each query neuron.

    dict
                    If `single_pred=True`: returns dictionary with
                    `(top_transmitter, confidence)` tuple for each query neuron.

    """
    # First get the synapses
    syn = fetch_synapses(x, pre=True, post=False, attach=False, min_score=None,
                         transmitters=True, live_query=live_query,
                         neuropils=neuropils is not None,
                         batch_size=batch_size,
                         dataset=dataset, **kwargs)

    if not isinstance(neuropils, type(None)):
        neuropils = make_iterable(neuropils)
        filter_in = [n for n in neuropils if not n.startswith('~')]
        filter_out = [n[1:] for n in neuropils if n.startswith('~')]

        if filter_in:
            syn = syn[syn.neuropil.isin(filter_in)]
        if filter_out:
            syn = syn[~syn.neuropil.isin(filter_out)]

        # Avoid setting-on-copy warning
        syn = syn.copy()

    # Process the predictions
    return collapse_nt_predictions(syn, single_pred=single_pred,
                                   weighted=weighted, id_col='pre')


def fetch_synapses(x, pre=True, post=True, attach=True, min_score=30, clean=True,
                   transmitters=False, neuropils=False, live_query=True,
                   batch_size=10, dataset='production', progress=True):
    """Fetch Buhmann et al. (2019) synapses for given neuron(s).

    Parameters
    ----------
    x :             int | list of int | Neuron/List
                    Either a FlyWire segment ID (i.e. root ID), a list thereof
                    or a Neuron/List. For neurons, the ``.id`` is assumed to be
                    the root ID. If you have a neuron (in FlyWire space) but
                    don't know its ID, use
                    :func:`fafbseg.flywire.neuron_to_segments` first.
    pre :           bool
                    Whether to fetch presynapses for the given neurons.
    post :          bool
                    Whether to fetch postsynapses for the given neurons.
    transmitters :  bool
                    Whether to also load per-synapse neurotransmitter predictions
                    from Eckstein et al. (2020).
    neuropils :     bool
                    Whether to add a column indicating which neuropil a synapse
                    is in.
    attach :        bool
                    If True and ``x`` is Neuron/List, the synapses will be added
                    as ``.connectors`` table. For TreeNeurons (skeletons), the
                    synapses will be mapped to the closest node. Note that the
                    function will still return the full synapse table.
    min_score :     int, optional
                    Minimum "cleft score". The default of 30 is what Buhmann et al.
                    used in the paper.
    clean :         bool
                    If True, we will perform some clean up of the connectivity
                    compared with the raw synapse information. Currently, we::
                        - drop autapses
                        - drop synapses from/to background (id 0)
                        - drop synapses that are >10um from the skeleton (only
                          if ``attach=True``)
    batch_size :    int
                    Number of IDs to query per batch. Too large batches might
                    lead to truncated tables: currently individual queries can
                    not return more than 200_000 rows and you will see a warning
                    if that limit is exceeded.
    live_query :    bool
                    Whether to query against the live data or against the latest
                    materialized table. The latter is useful if you are working
                    with IDs that you got from another annotation table. Using
                    the live query is much slower!
    dataset :       str | CloudVolume
                    Against which FlyWire dataset to query::
                        - "production" (current production dataset, fly_v31)
                        - "sandbox" (i.e. fly_v26)

    Returns
    -------
    pandas.DataFrame
                    Note that each synapse (or rather synaptic connection)
                    will show up only once. Depending on the query neurons
                    (`x`), a given row might represent a presynapse for one and
                    a postsynapse for another neuron.


    Examples
    --------

    Fetch synapses for a given root ID

    >>> from fafbseg import flywire
    >>> syn = flywire.fetch_synapses(720575940642744480)
    >>> syn.head()
               id valid   pre_x   pre_y  ...       oct       ser        da
    0   178959090     t  488248  238240  ...  0.000532  0.000015  0.000346
    2   205400582     t  469592  240224  ...  0.001383  0.005552  0.023057
    4    68853638     t  442348   86348  ...  0.000002  0.000441  0.023308
    7   176752216     t  455640  214792  ...  0.000039  0.066771  0.086935
    10  178997778     t  473376  239832  ...  0.006675  0.000100  0.002978

    Skeletonize a neuron and attach its synapses

    >>> from fafbseg import flywire
    >>> sk = flywire.skeletonize_neuron(720575940642744480)
    >>> _ = flywire.fetch_synapses(sk, attach=True)
    >>> sk.connectors.head()
       connector_id       x       y       z  cleft_score          partner_id type  node_id
    0             0  438416   95608  150240          117  720575940385508863  pre     2896
    1             1  439776   89464  159680          152  720575940386246908  pre     3009
    2             2  435140   94556  151640          139  720575940613778326  pre     2562
    3             3  384384  100996  160960          146  720575940451774747  pre      843
    4             4  448676   97180  148160          141  720575940637824189  pre     4344

    """
    if not pre and not post:
        raise ValueError('`pre` and `post` must not both be False')

    # Parse root IDs
    ids = parse_root_ids(x)

    # Get the cave client
    client = get_cave_client(dataset=dataset)

    # Check if any of these root IDs are outdated
    if live_query:
        # For live queries we just need to make sure the root IDs are up-to-date
        not_latest = ids[~is_latest_root(ids, dataset=dataset)]
        if any(not_latest):
            print('Some root IDs are outdated and synapse/connectivity will be '
                  f'inaccurrate:\n\n {", ".join(not_latest.astype(str))}\n\n'
                  'Try updating the root IDs using e.g. `flywire.update_ids` '
                  'or `flywire.supervoxels_to_roots` if you have supervoxel IDs.')
    else:
        # For non-live queries we need to worry about two things:
        # 1. Was the root ID already outdated when the materialization happened
        ts_m = client.materialize.get_timestamp()
        not_latest = ids[~client.chunkedgraph.is_latest_roots(ids, timestamp=ts_m)]
        if any(not_latest):
            print('Some root IDs were already outdated at the latest '
                  'materialization and synapse/connectivity data will be '
                  f'inaccurrate:\n\n {", ".join(not_latest.astype(str))}\n\n'
                  'Try updating the root IDs using e.g. `flywire.update_ids` '
                  'or `flywire.supervoxels_to_roots` if you have supervoxel IDs.')

        # 2. Is the root ID more recent than the materialization
        ts_r = client.chunkedgraph.get_root_timestamps(ids)
        too_recent = ids[ts_r > ts_m]
        if any(too_recent):
            print('Some root IDs are more recent than the latest '
                  'materialization and synapse/connectivity data will be '
                  f'inaccurate:\n\n {", ".join(too_recent.astype(str))}\n\n'
                  'You can either try mapping these IDs back in time or use'
                  '`live_query=True`.')

    columns = ['pre_pt_root_id', 'post_pt_root_id', 'cleft_score',
               'pre_pt_position', 'post_pt_position', 'id']

    if transmitters:
        columns += ['gaba', 'ach', 'glut', 'oct', 'ser', 'da']

    if live_query:
        func = partial(retry(client.materialize.live_query),
                       table=client.materialize.synapse_table,
                       timestamp=dt.datetime.utcnow(),
                       split_positions=True,
                       select_columns=columns)
    else:
        func = partial(retry(client.materialize.query_table),
                       table=client.materialize.synapse_table,
                       split_positions=True,
                       select_columns=columns)

    syn = []
    for i in trange(0, len(ids), batch_size,
                    desc='Fetching synapses',
                    disable=not progress or len(ids) <= batch_size):
        batch = ids[i:i+batch_size]
        if post:
            syn.append(func(filter_in_dict=dict(post_pt_root_id=batch)))
        if pre:
            syn.append(func(filter_in_dict=dict(pre_pt_root_id=batch)))

    # Drop attrs to avoid issues when concatenating
    for df in syn:
        df.attrs = {}

    # Combine results from batches
    syn = pd.concat([s for s in syn if not s.empty], axis=0, ignore_index=True)

    # Depending on how queries were batched, we need to drop duplicate synapses
    syn.drop_duplicates('id', inplace=True)

    # Rename some of those columns
    syn.rename({'post_pt_root_id': 'post',
                'pre_pt_root_id': 'pre',
                'post_pt_position_x': 'post_x',
                'post_pt_position_y': 'post_y',
                'post_pt_position_z': 'post_z',
                'pre_pt_position_x': 'pre_x',
                'pre_pt_position_y': 'pre_y',
                'pre_pt_position_z': 'pre_z',
                },
               axis=1, inplace=True)

    if transmitters:
        syn.rename({'ach': 'acetylcholine',
                    'glut': 'glutamate',
                    'oct': 'octopamine',
                    'ser': 'serotonin',
                    'da': 'dopamine'},
                   axis=1, inplace=True)

    # Next we need to run some clean-up:
    # Drop below threshold connections
    if min_score:
        syn = syn[syn.cleft_score >= min_score]

    if clean:
        # Drop autapses
        syn = syn[syn.pre != syn.post]
        # Drop connections involving 0 (background, glia)
        syn = syn[(syn.pre != 0) & (syn.post != 0)]

    # Avoid copy warning
    syn = syn.copy()

    if neuropils:
        syn['neuropil'] = get_synapse_areas(syn['id'].values)
        syn['neuropil'] = syn.neuropil.astype('category')

    # Drop ID column
    # syn.drop('id', axis=1, inplace=True)

    if isinstance(x, navis.core.BaseNeuron):
        x = navis.NeuronList([x])

    if attach and isinstance(x, navis.NeuronList):
        for n in x:
            presyn = postsyn = pd.DataFrame([])
            add_cols = ['neuropil'] if neuropils else []
            if pre:
                cols = ['pre_x', 'pre_y', 'pre_z',
                        'cleft_score', 'post'] + add_cols
                presyn = syn.loc[syn.pre == np.int64(n.id), cols
                                 ].rename({'pre_x': 'x',
                                           'pre_y': 'y',
                                           'pre_z': 'z',
                                           'post': 'partner_id'},
                                          axis=1)
                presyn['type'] = 'pre'
            if post:
                cols = ['post_x', 'post_y', 'post_z',
                        'cleft_score', 'pre'] + add_cols
                postsyn = syn.loc[syn.post == np.int64(n.id), cols
                                  ].rename({'post_x': 'x',
                                            'post_y': 'y',
                                            'post_z': 'z',
                                            'pre': 'partner_id'},
                                           axis=1)
                postsyn['type'] = 'post'

            connectors = pd.concat((presyn, postsyn), axis=0, ignore_index=True)

            # Turn type column into categorical to save memory
            connectors['type'] = connectors['type'].astype('category')

            # If TreeNeuron, map each synapse to a node
            if isinstance(n, navis.TreeNeuron):
                tree = navis.neuron2KDTree(n, data='nodes')
                dist, ix = tree.query(connectors[['x', 'y', 'z']].values)

                too_far = dist > 10_000
                if any(too_far) and clean:
                    connectors = connectors[~too_far].copy()
                    ix = ix[~too_far]

                connectors['node_id'] = n.nodes.node_id.values[ix]

                # Add an ID column for navis' sake
                connectors.insert(0, 'connector_id', np.arange(connectors.shape[0]))

            n.connectors = connectors

    return syn


def fetch_adjacency(sources, targets=None, min_score=30, live_query=True,
                    neuropils=None, batch_size=1000, dataset='production',
                    progress=True):
    """Fetch adjacency matrix.

    Parameters
    ----------
    sources :       int | list of int | Neuron/List
                    Either FlyWire segment ID (i.e. root ID), a list thereof
                    or a Neuron/List. For neurons, the ``.id`` is assumed to be
                    the root ID. If you have a neuron (in FlyWire space) but
                    don't know its ID, use :func:`fafbseg.flywire.neuron_to_segments`
                    first.
    targets :       int | list of int | Neuron/List, optional
                    Either FlyWire segment ID (i.e. root ID), a list thereof
                    or a Neuron/List. For neurons, the ``.id`` is assumed to be
                    the root ID. If you have a neuron (in FlyWire space) but
                    don't know its ID, use :func:`fafbseg.flywire.neuron_to_segments`
                    first. If ``None``, will assume ```targets = sources``.
    min_score :     int
                    Minimum "cleft score". The default of 30 is what Buhmann et al.
                    used in the paper.
    neuropils :     str | list of str, optional
                    Provide neuropil (e.g. ``'AL_R'``) or list thereof (e.g.
                    ``['AL_R', 'AL_L']``) to filter connectivity to these ROIs.
                    Prefix neuropil with a tilde (e.g. ``~AL_R``) to exclude it.
    batch_size :    int
                    Number of IDs to query per batch. Too large batches can
                    lead to truncated tables: currently individual queries do
                    not return more than 200_000 connections. If you see a
                    warning that this limit has been exceeded, decrease the
                    batch size!
    live_query :    bool
                    Whether to query against the live data or against the latest
                    materialized table. The latter is useful if you are working
                    with IDs that you got from another annotation table.
    dataset :       str | CloudVolume
                    Against which FlyWire dataset to query::
                        - "production" (current production dataset, fly_v31)
                        - "sandbox" (i.e. fly_v26)

    Returns
    -------
    adjacency :     pd.DataFrame
                    Adjacency matrix. Rows (sources) and columns (targets) are
                    in the same order as input.

    """
    if isinstance(targets, type(None)):
        targets = sources

    # Parse root IDs
    sources = parse_root_ids(sources)
    targets = parse_root_ids(targets)
    both = np.unique(np.append(sources, targets))

    client = get_cave_client(dataset=dataset)

    # Check if any of these root IDs are outdated
    if live_query:
        not_latest = both[~is_latest_root(both, dataset=dataset)]
        if any(not_latest):
            print(f'Root ID(s) {", ".join(not_latest.astype(str))} are outdated '
                  'and connectivity might be inaccurrate.')
    else:
        ts_m = client.materialize.get_timestamp()
        ts_r = client.chunkedgraph.get_root_timestamps(ids)
        too_recent = ids[ts_r > ts_m]
        if any(too_recent):
            print(f'Root ID(s) {", ".join(too_recent.astype(str))} are more '
                  'recent than the latest materialization. You can either try '
                  'mapping these IDs back in time or use `live_query=True`')

    columns = ['pre_pt_root_id', 'post_pt_root_id', 'cleft_score']
    if live_query:
        func = partial(retry(client.materialize.live_query),
                       table=client.materialize.synapse_table,
                       timestamp=dt.datetime.utcnow(),
                       select_columns=columns)
    else:
        func = partial(retry(client.materialize.query_table),
                       table=client.materialize.synapse_table,
                       select_columns=columns)

    syn = []
    for i in trange(0, len(sources), batch_size,
                    desc='Fetching adjacency',
                    disable=not progress or len(sources) <= batch_size):
        source_batch = sources[i:i+batch_size]
        for k in range(0, len(targets), batch_size):
            target_batch = targets[k:k+batch_size]

            this = func(filter_in_dict=dict(post_pt_root_id=target_batch,
                                            pre_pt_root_id=source_batch))

            # We need to drop the .attrs (which contain meta data from queries)
            # Otherwise we run into issues when concatenating
            this.attrs = {}

            if not this.empty:
                syn.append(this)

    # Combine results from batches
    if len(syn):
        syn = pd.concat(syn, axis=0, ignore_index=True)
    else:
        adj = pd.DataFrame(np.zeros((len(sources), len(targets))),
                           index=sources, columns=targets)
        adj.index.name = 'source'
        adj.columns.name = 'target'
        return adj

    # Depending on how queries were batched, we need to drop duplicate synapses
    syn.drop_duplicates('id', inplace=True)

    # Subset to the desired neuropils
    if not isinstance(neuropils, type(None)):
        neuropils = make_iterable(neuropils)

        if len(neuropils):
            filter_in = [n for n in neuropils if not n.startswith('~')]
            filter_out = [n[1:] for n in neuropils if n.startswith('~')]

            syn['neuropil'] = get_synapse_areas(syn['id'].values)
            syn['neuropil'] = syn.neuropil.astype('category')

            if filter_in:
                syn = syn[syn.neuropil.isin(filter_in)]
            if filter_out:
                syn = syn[~syn.neuropil.isin(filter_out)]

            syn = syn.copy()

    # Rename some of those columns
    syn.rename({'post_pt_root_id': 'post', 'pre_pt_root_id': 'pre'},
               axis=1, inplace=True)

    # Next we need to run some clean-up:
    # Drop below threshold connections
    if min_score:
        syn = syn[syn.cleft_score >= min_score]

    # Aggregate
    cn = syn.groupby(['pre', 'post'], as_index=False).size()
    cn.columns = ['source', 'target', 'weight']

    # Pivot
    adj = cn.pivot(index='source', columns='target', values='weight').fillna(0)

    # Index to match order and add any missing neurons
    adj = adj.reindex(index=sources, columns=targets).fillna(0)

    return adj


def fetch_connectivity(x, clean=True, style='simple', min_score=30,
                       upstream=True, downstream=True, transmitters=False,
                       neuropils=None, batch_size=30, live_query=True,
                       dataset='production', progress=True):
    """Fetch Buhmann et al. (2019) connectivity for given neuron(s).

    Parameters
    ----------
    x :             int | list of int | Neuron/List
                    Either a FlyWire root ID, a list thereof or a Neuron/List.
                    For neurons, the ``.id`` is assumed to be the root ID. If
                    you have a neuron (in FlyWire space) but don't know its ID,
                    use :func:`fafbseg.flywire.neuron_to_segments` first.
    clean :         bool
                    If True, we will perform some clean up of the connectivity
                    compared with the raw synapse information. Currently, we::
                        - drop autapses
                        - drop synapses from/to background (id 0)

    style :         "simple" | "catmaid"
                    Style of the returned table.
    min_score :     int
                    Minimum "cleft score". The default of 30 is what Buhmann et al.
                    used in the paper.
    upstream :      bool
                    Whether to fetch upstream connectivity of ```x``.
    downstream :    bool
                    Whether to fetch downstream connectivity of ```x``.
    transmitters :  bool
                    If True, will attach the best guess for the transmitter
                    for a given connection based on the predictions in Eckstein
                    et al (2020). IMPORTANT: the predictions are based solely on
                    the connections retrieved as part of this query which likely
                    represent only a fraction of each neuron's total synapses.
                    As such the predictions need to be taken with a grain
                    of salt - in particular for weak connections!
                    To get the "full" predictions see
                    :func:`fafbseg.flywire.predict_transmitter`.
    neuropils :     str | list of str, optional
                    Provide neuropil (e.g. ``'AL_R'``) or list thereof (e.g.
                    ``['AL_R', 'AL_L']``) to filter connectivity to these ROIs.
                    Prefix neuropil with a tilde (e.g. ``~AL_R``) to exclude it.
    batch_size :    int
                    Number of IDs to query per batch. Too large batches might
                    lead to truncated tables: currently individual queries can
                    not return more than 200_000 rows and you will see a warning
                    if that limit is exceeded.
    live_query :    bool
                    Whether to query against the live data or against the latest
                    materialized table. The latter is useful if you are working
                    with IDs that you got from another annotation table.
    dataset :       str | CloudVolume
                    Against which FlyWire dataset to query::
                        - "production" (current production dataset, fly_v31)
                        - "sandbox" (i.e. fly_v26)


    Returns
    -------
    pd.DataFrame
                Connectivity table.

    """
    if not upstream and not downstream:
        raise ValueError('`upstream` and `downstream` must not both be False')

    if transmitters and style == 'catmaid':
        raise ValueError('`style` must be "simple" when asking for transmitters')

    # Parse root IDs
    ids = parse_root_ids(x)

    client = get_cave_client(dataset=dataset)

    # Check if any of these root IDs are outdated
    if live_query:
        not_latest = ids[~is_latest_root(ids, dataset=dataset)]
        if any(not_latest):
            print(f'Root ID(s) {", ".join(not_latest.astype(str))} are outdated '
                  'and live connectivity might be inaccurrate.')
    else:
        ts_m = client.materialize.get_timestamp()
        ts_r = client.chunkedgraph.get_root_timestamps(ids)
        too_recent = ids[ts_r > ts_m]
        if any(too_recent):
            print(f'Root ID(s) {", ".join(too_recent.astype(str))} are more '
                  'recent than the latest materialization. You can either try '
                  'mapping these IDs back in time or use `live_query=True`')

    columns = ['pre_pt_root_id', 'post_pt_root_id', 'cleft_score']

    if transmitters:
        columns += ['gaba', 'ach', 'glut', 'oct', 'ser', 'da']

    if live_query:
        func = partial(retry(client.materialize.live_query),
                       table=client.materialize.synapse_table,
                       timestamp=dt.datetime.utcnow(),
                       select_columns=columns)
    else:
        func = partial(retry(client.materialize.query_table),
                       table=client.materialize.synapse_table,
                       select_columns=columns)

    syn = []
    for i in trange(0, len(ids), batch_size,
                    desc='Fetching connectivity',
                    disable=not progress or len(ids) <= batch_size):
        batch = ids[i:i+batch_size]
        if upstream:
            syn.append(func(filter_in_dict=dict(post_pt_root_id=batch)))
        if downstream:
            syn.append(func(filter_in_dict=dict(pre_pt_root_id=batch)))

    # Drop attrs to avoid issues when concatenating
    for df in syn:
        df.attrs = {}

    # Combine results from batches
    syn = pd.concat([s for s in syn if not s.empty], axis=0, ignore_index=True)

    # Subset to the desired neuropils
    if not isinstance(neuropils, type(None)):
        neuropils = make_iterable(neuropils)

        if len(neuropils):
            filter_in = [n for n in neuropils if not n.startswith('~')]
            filter_out = [n[1:] for n in neuropils if n.startswith('~')]

            syn['neuropil'] = get_synapse_areas(syn['id'].values)
            syn['neuropil'] = syn.neuropil.astype('category')

            if filter_in:
                syn = syn[syn.neuropil.isin(filter_in)]
            if filter_out:
                syn = syn[~syn.neuropil.isin(filter_out)]

            syn = syn.copy()

    # Rename some of those columns
    syn.rename({'post_pt_root_id': 'post', 'pre_pt_root_id': 'pre'},
               axis=1, inplace=True)

    if transmitters:
        syn.rename({'ach': 'acetylcholine',
                    'glut': 'glutamate',
                    'oct': 'octopamine',
                    'ser': 'serotonin',
                    'da': 'dopamine'},
                   axis=1, inplace=True)

    # Next we need to run some clean-up:
    # Drop below threshold connections
    if min_score:
        syn = syn[syn.cleft_score >= min_score]

    if clean:
        # Drop autapses
        syn = syn[syn.pre != syn.post]
        # Drop connections involving 0 (background, glia)
        syn = syn[(syn.pre != 0) & (syn.post != 0)]

    # Turn into connectivity table
    cn_table = syn.groupby(['pre', 'post'], as_index=False).size().rename({'size': 'weight'}, axis=1)

    # Style
    if style == 'catmaid':
        cn_table = catmaid_table(cn_table, query_ids=ids)
    else:
        cn_table.sort_values('weight', ascending=False, inplace=True)
        cn_table.reset_index(drop=True, inplace=True)

    if transmitters:
        # Avoid copy warning
        syn = syn.copy()

        # Generate per-neuron predictions
        pred = collapse_nt_predictions(syn, single_pred=True, id_col='pre')

        cn_table['pred_nt'] = cn_table.pre.map(lambda x: pred.get(x, [None])[0])
        cn_table['pred_conf'] = cn_table.pre.map(lambda x: pred.get(x, [None, None])[1])

    return cn_table
