import numpy as np

class BasicTerrain:    
    def __init__(self, params, lower_layer_mask):
        self._params = {}
        self.params = params
        self._lower_layer_mask = None
        self.lower_layer_mask = lower_layer_mask

    def __str__(self):
        return str(self.__dict__)
    
    def _verify_layer(self, layer, layer_name = "layer"):
        if type(layer) != np.ndarray:
            raise TypeError(f"{layer_name} is not numpy ndarray type")
        if layer.ndim != 2:
            raise TypeError(f"{layer_name} is not 2d array")

    def _verify_layer_mask(self, layer_mask, layer_mask_name = "layer_mask"):
        _verify_layer(layer_mask, layer_mask_name)
        if layer.dtype != bool:
            raise TypeError(f"{layer_name} dtype is not a boolean")

    def generate_layer(self, seed):
        layer_mask = self.lower_layer_mask
        return layer_mask
        
    @property
    def lower_layer(self):
        return self._lower_layer
    
    @lower_layer.setter
    def lower_layer(self, lower_layer):
        self._verify_layer(lower_layer, "lower_layer")
        self._lower_layer = lower_layer

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        if params is None:
            params = {}
        if type(params) != dict:
            raise TypeError("basic terrain can handle dict or None types as params")
        if len(params) != 0:
            raise ValueError("basic terrain does not need parameters")
        self._params = {}

    @property
    def count(self):
        return self._params['count']
        
    @count.setter
    def count(self, count):
        if(type(count) != int):
            raise TypeError("count is not an integer")
        if(count < 0):
            raise ValueError("count has wrong value")
        self._params['count'] = count 
 
    @property
    def color(self):
        return self._params['color']
    
    @color.setter
    def color(self, color):
        if(type(color) != str):
            raise TypeError("color is not a string")
        self._params['color'] = color
 
    @property
    def percentage(self):
        return self._params['percentage']
    
    @percentage.setter
    def percentage(self, percentage):
        if(type(percentage) != float):
            raise TypeError("percentage is not a float")
        if(percentage < 0. or percentage >1.):
            raise ValueError("percentage has wrong value")
        self._params['percentage'] = percentage 

class Island(BasicTerrain):
    def __init__(self, params, lower_layer):
        super().__init__(params, lower_layer)
        
    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params): 
        if 'count' not in params or 'color' not in params or 'percentage' not in params:
            raise ValueError("parameters given to params setter are not vaild")
        try:
            self.count = params['count']
            self.color = params['color'];
            self.percentage = params['percentage']
        except TypeError as err:
            raise ValueError("parameters values given to params setter are not vaild:" + "\nTypeError: " + str(err))
        except ValueError as err:            
            raise ValueError("parameters values given to params setter are not vaild" + "\nValueError: " + str(err))
lower_layer = np.ones((30,15),dtype=bool)
a = BasicTerrain({},lower_layer )
