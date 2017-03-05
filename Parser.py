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
        self._temporal_coord = None

        # combined data dictionary of all variables and coords
        # example: {"x":data, "t":data, "u":data}
        self._data = None

        # maximum time derivative order (d/dt=1)
        # example: 1
        self._temporal_deriv_order = None

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
        self.parseEquation()
        self.countTemporalDerivOrder()


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
        sections = ["equation", "parameters", "spatial_coord_names", "spatial_coord_ordering","temporal_coord_name"]
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
                self._field_names[key] = param_str.strip()


        # read in time coordinate name
        if (len(cp["temporal_coord_name"].keys()) > 1):
            raise IOError("Improper config file: must have at most 1 time coordinate")
        self._temporal_coord = list(cp["temporal_coord_name"].keys())[0].strip()
        self._field_names.update(cp["temporal_coord_name"])

        # read in spatial coordinate names and ordering
        spatial_coords_unordered = cp["spatial_coord_names"].keys()
        if ("spatial_coord_ordering" not in cp["spatial_coord_ordering"].keys()):
            raise IOError("Improper config file: missing spatial_coord_ordering")
        spatial_coord_ordering_str = cp["spatial_coord_ordering"]["spatial_coord_ordering"].strip()
        spatial_coord_ordering = list(map(str.strip,spatial_coord_ordering_str.split(",")))
        if (set(spatial_coord_ordering) != set(spatial_coords_unordered)):
            raise IOError("Improper config file: spatial_coord_ordering does not match spatial_coords")
        self._spatial_coords = spatial_coord_ordering
        self._field_names.update(cp["spatial_coord_names"])


    def parseEquation(self):
        if (self._eqn_string == None):
            raise ValueError("Equation string not yet initialized (did you call readConfigFile?)")
        import re
        equation = self._eqn_string

        # all available variables in brackets, e.g. [xyt]
        vars_re = "[" + "".join(self._spatial_coords) + self._temporal_coord + "]"

        # match {x,2} and x
        Dvars_re = "({\s*(" + vars_re + ")\s*,\s*([0-9]+)\s*}|" + vars_re + ")"

        # TODO: right now this prevents any variabls from having a name with capital D in it.
        # This regex should be improved so that that is all right.
        Deriv_re_str ="D\[([^,D]*?),\s*" + Dvars_re + "\s*\]"

        # replace all derivatives with coded versions
        code_equation = equation
        Deriv_search = True
        while(Deriv_search):
            Deriv_search = re.search(Deriv_re_str,code_equation)
            if(Deriv_search):
                matched_str = Deriv_search.group(0)
                internal_groups = Deriv_search.groups()
                derivand = internal_groups[0]
                if (internal_groups[2] == None):
                    var = internal_groups[1]
                    order = 1
                else:
                    var = internal_groups[2]
                    order = int(internal_groups[3])
                #print("::::  Match  ::::")
                #print(matched_str)
                #print(derivand + " ::: " + var + " ::: " + str(order))

                # construct the parsed code version of the derivative operators
                code_derivop = ""
                for j in range(0,order):
                    code_derivop += "deriv[\"%s\"] @ " % var
                code_version = "( %s ( %s ) )" % (code_derivop, derivand)
                #print(code_version)

                # substitute the result into code_equation
                code_equation = code_equation.replace(matched_str, code_version)
                #print(code_equation)
                #print("::::End Match::::")


        # construct the parsed code version of the entire equation
        for param in self._parameters.keys():
            param_val_str = "(" + str(self._parameters[param]) + ")"
            param_re = "\\b%s\\b" % param
            code_equation = re.sub(param_re, param_val_str, code_equation)
        for fieldvar in self._field_names.keys():
            fieldvar_str = " data[\"%s\"] " % fieldvar
            fieldvar_re = "(?!\")\\b%s\\b(?!\")" % fieldvar
            code_equation = re.sub(fieldvar_re, fieldvar_str, code_equation)

        #print(code_equation)
        self._eqn_parsed = code_equation


    def countInteriorTemporalDerivs(self, substr, level):
        import re

        # to make things easier, replace all commas in {x,3} with semicolons
        Dcomma_re = "({[^,]*),(\s*[0-9]+\s*})"
        substr = re.sub(Dcomma_re, r"\1;\2",substr)

        # match t and {t,3}
        Dvars_re = "({\s*" + self._temporal_coord + "\s*;\s*([0-9]+)\s*}|" + self._temporal_coord + ")"
        # inD tells whether or not we're in an outer derivative
        inD = False
        parcount = 0
        subsubs = []
        subsub = ""
        for c in substr:
            if (not inD):
                if c == "D":
                    inD = True
            else:
                subsub += c
                if c == "[":
                    parcount += 1
                if c == "]":
                    parcount -= 1
                    if parcount == 0:
                        inD = False
                        subsubs.append(subsub)
                        subsub = ""

        new_sub_tuples = []
        for ss in subsubs:
            this_level = level
            ss = ss[1:-1]
            ss_split = ss.split(",")
            derivand = ",".join(ss_split[0:-1])
            varstr = ss_split[-1]

            Deriv_search = re.search(Dvars_re, varstr)
            if (Deriv_search):
                #matched_str = Deriv_search.group(0)
                internal_groups = Deriv_search.groups()
                if (internal_groups[1] == None):
                    this_level += 1
                else:
                    this_level += int(internal_groups[1])
            new_sub_tuples.append( (derivand, this_level) )

        max_level = level
        for (s,l) in new_sub_tuples:
            this_level = self.countInteriorTemporalDerivs(s,l)
            #print(level,s,this_level)
            if ( this_level > max_level ):
                max_level = this_level

        return max_level

    def countTemporalDerivOrder(self):
        if (self._eqn_string == None):
            raise ValueError("Equation string not yet initialized (did you call readConfigFile?)")
        equation = self._eqn_string

        self._temporal_deriv_order = self.countInteriorTemporalDerivs(equation,0)











