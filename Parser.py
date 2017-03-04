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

        # ok seems safe to proceed to reading the config file
        import configparser
        cp = configparser.ConfigParser()
        cp.read(config_file_name)

        sections_found = cp.sections()
        # the config file must have the correct case. sorry.
        # DO NOT IMPLEMENT: sections_found = list(map(str.lower,sections_found))

        # first, make sure that the required sections are present (and ignore any others)
        sections = ["equation", "parameters", "spatial_coord_names", "time_coord_name"]
        if not ( len( set(cp.sections()) & set(sections) ) == len(sections) ):
            raise IOError("Improper config file. Section titles must be exactly " + str(sections))

        # read in equation
        if ("equation" not in cp["equation"].keys()):
            raise IOError("Improper config file: missing equation")
        self._eqn_string = cp["equation"]["equation"]

        # set field_names to an empty dictionary; now we will populate it with the parameters etc.
        self._field_names = {}
        self._parameters = {}

        # read in parameters
        for key in cp["parameters"]:
            try:
                param_val = cp["parameters"].getfloat(key)
                self._parameters[key] = param_val
            except ValueError:
                param_str = cp["parameters"][key]
                self._field_names[key] = param_str


        # read in spatial coordinate names
        self._spatial_coords = cp["spatial_coord_names"].keys()
        self._field_names.update(cp["spatial_coord_names"])

        # read in time coordinate name
        if (len(cp["time_coord_name"].keys()) > 1):
            raise IOError("Improper config file: must have at most 1 time coordinate")
        self._time_coord = list(cp["time_coord_name"].keys())[0]
        self._field_names.update(cp["time_coord_name"])
