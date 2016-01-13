import numpy as _numpy
from . import internal as _internal

def get_default_parameters(num_points, dimension, distance='euclidean_squared', is_sufficiently_random=False):
    return _internal.get_default_parameters(num_points, dimension, distance, is_sufficiently_random)

def compute_number_of_hash_functions(num_bits, params):
    _internal.compute_number_of_hash_functions(num_bits, params)

class LSHIndex:
    def __init__(self, params):
        self._params = params
        self._dataset = None
        self._table = None

    def fit(self, dataset):
        if not isinstance(dataset, _numpy.ndarray):
            raise TypeError('dataset must be an instance of numpy.ndarray')
        if len(dataset.shape) != 2:
            raise ValueError('dataset must be a two-dimensional array')
        if dataset.dtype != _numpy.float32 and dataset.dtype != _numpy.float64:
            raise ValueError('dataset must consist of floats or doubles')
        if dataset.shape[1] != self._params.dimension:
            raise ValueError('dataset dimension mismatch: {} expected, but {} found'.format(self._params.dimension, dataset.shape[1]))
        self._dataset = dataset
        if dataset.dtype == _numpy.float32:
            self._table = _internal.construct_table_dense_float(dataset, self._params)
        else:
            self._table = _internal.construct_table_dense_double(dataset, self._params)

    def _check_query(self, query):
        if not isinstance(query, _numpy.ndarray):
            raise TypeError('query must be an instance of numpy.ndarray')
        if len(query.shape) != 1:
            raise ValueError('query must be one-dimensional')
        if self._dataset.dtype != query.dtype:
            raise ValueError('dataset and query must have the same dtype')
        if query.shape[0] != self._params.dimension:
            raise ValueError('query dimension mismatch: {} expected, but {} found'.format(self._params.dimension, query.shape[0]))

    def find_k_nearest_neighbors(self, query, k):
        self._check_query(query)
        return self._table.find_k_nearest_neighbors(query, k)
        
    def find_near_neighbors(self, query, threshold):
        self._check_query(query)
        return self._table.find_near_neighbors(query, threshold)
        
    def find_nearest_neighbor(self, query):
        self._check_query(query)
        return self._table.find_nearest_neighbor(query)
        
    def get_candidates_with_duplicates(self, query):
        self._check_query(query)
        return self._table.get_candidates_with_duplicates(query)
        
    def get_max_num_candidates(self):
        return self._table.get_max_num_candidates()
        
    def get_num_probes(self):
        return self._table.get_num_probes()
        
    def get_query_statistics(self):
        return self._table.get_query_statistics()
        
    def get_unique_candidates(self, query):
        self._check_query(query)
        return self._table.get_unique_candidates(query)
        
    def get_unique_sorted_candidates(self):
        return self._table.get_unique_sorted_candidates(query)
        
    def reset_query_statistics(self):
        self._table.reset_query_statistics()
        
    def set_max_num_candidates(self, max_num_candidates):
        self._table.set_max_num_candidates(max_num_candidates)
        
    def set_num_probes(self, num_probes):
        if num_probes < self._params.l:
            raise ValueError('number of probes must be at least the number of tables ({})'.format(self._params.l))
        self._table.set_num_probes(num_probes)
