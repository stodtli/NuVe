# Parser.py

import os.path

class Parser(object):
    def __init__(self, config_file_name):
        # list of numerical parameters from the config file
        # example: {"nu":1.0}
        self._parameters = None

        # list of mappings from the user's variables (as used in the equation)
        # to field names in the data file.
        # example: {"u":"U1", "x":"X1", "y":Y1", "mu":"MU", "t":"T"}
        self._field_names = None

        # list of spatial coordinate names
        # example: ["x","y","z"]
        self._spatial_coords = None

        # time coordinate name
        # example: "t"
        self._time_coord = None

        # combined data dictionary of all variables and coords
        # example: {"x":data, "t":data, "u":data}
        self._data = None

        # maximum time derivative order (d/dt=1)
        # example: 1
        self._time_deriv_order = None

        # list of derivatives to pass to DMatrix
        # example: ["x","t"]
        self._derivs_needed = None

        # the string equation to parse
        # example: "D[u,{x,2}] = nu*D[u,t]"
        self._eqn_string = None

        # the parsed equation string
        # example: 'matmul(deriv["x"][2], data["u"]) - nu * matmul(deriv["t"][1], data["u"])'
        self._eqn_parsed = None

        self.readConfigFile(config_file_name)

    def readConfigFile(self, config_file_name):

        # Check that config_file_name is a string
        if (type(config_file_name) != str):
            raise TypeError('config_file_name must be a string')

        # Check that config_file_name exists and has ok permissions
        if not (os.path.isfile(config_file_name) and os.access(config_file_name, os.R_OK)):
            raise IOError('file "' + config_file_name + '" does not exist or cannot be accessed')

        import ConfigParser
        cp = ConfigParser.ConfigParser()
        cp.read(config_file_name)
