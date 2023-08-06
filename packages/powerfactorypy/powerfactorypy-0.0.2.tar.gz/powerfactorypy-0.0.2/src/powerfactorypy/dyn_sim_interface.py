from base_interface import PFBaseInterface

class PFDynSimInterface(PFBaseInterface):
  
  def __init__(self,app): 
    self.app = app
    self.export_path = ""
    self.csv_export_file_name = "SimulationResults.csv"    
    self.results = "All calculations.ElmRes"
    self.simulation_events_folder_name = "Simulation Events/Fault.IntEvt"
    self.simulation_events_folder = None
    self.dynamic_model_templates_path = r"Library\Dynamic Models"

  def export_to_csv(self):
    """
    Exports the simulation results in self.results to csv.
    *ToDo better explanation ftarget file path
    """
    comRes = self.app.GetFromStudyCase("ComRes")
    comRes.pResult = self.app.GetFromStudyCase(self.results)
    comRes.iopt_exp = 6 # to export as csv
    comRes.f_name = self.export_path + "\\" + self.csv_export_file_name
    comRes.iopt_sep = 1 # to use the system seperator
    comRes.iopt_honly = 0 # to export data and not only the header
    comRes.iopt_csel = 0 # export all variables 
    comRes.iopt_locn = 3 # column header includes path
    comRes.ciopt_head = 1 # full variable name
    comRes.Execute()
    self.format_csv()
          
  def format_csv(self):
    """
    Formats the csv file as exported from PowerFactory.
    PF uses two columns at the top for object and variabel name.
    This is reduced to one column that contains all the information.
    The first time column is named 'Time'. 
    """
    csv_path = self.export_path + '\\' + self.csv_export_file_name
    with open(csv_path) as file:
      csv_file = pd.read_csv(file) 
      new_headers = []
      for header in csv_file: 
        variable = csv_file[header][0]
        new_header = self.format_full_path(header)
        new_headers.append(new_header + '.' + variable)
      new_headers[0] = 'Time'
      csv_file.columns = new_headers
      csv_file.drop(0,axis=0,inplace=True) # delete first column containing indexes
      csv_file.to_csv(csv_path+".csv",index=False)
    remove(csv_path)
  
  def initialize_dyn_sim(self,param=None):
    """
    Initialize time domain simulation.
    Parameters for 'ComInc' command object can be specified in 'param' dictionary.
    """
    cominc = self.app.GetFromStudyCase("ComInc")
    if param is not None:
      self.set_attr(cominc,param)
    cominc.Execute()

  def sim(self,param=None):
    """
    Perform dynamic simulation.
    Parameters for 'ComSim' command object can be specified in 'param' dictionary.
    """
    comsim = self.app.GetFromStudyCase("ComSim")
    if param != None:
      self.set_attr(comsim,param)
    comsim.Execute()

  def initialize_and_sim(self):
    """Initialize and perform time domain simulation."""
    self.initialize_dyn_sim()
    self.sim()

  def create_parameter_event(self,target,variable,steps,name="ParEvt"):
    if not isinstance(steps, list):
      steps = [steps]
    if self.simulation_events_folder is None:
      self.get_simulation_events_folder()
    target = self.return_obj_if_path_is_provided(target)
    for step in steps:
      event = self.create_in_folder(self.simulation_events_folder,name+".EvtParam")
      event.p_target = target
      event.time = step[0]
      event.variable = variable
      event.value = str(step[1])

  def get_simulation_events_folder(self):
    self.simulation_events_folder = (
      self.app.GetFromStudyCase(self.simulation_events_folder_name))

  def create_reference_signal(self,path,points):
    composite_model = self.create_by_path(path + ".ElmComp")
    composite_frame = self.get_obj(self.dynamic_model_teamplates_path +
      r"\reference_signal_frame")
    composite_model.SetAttribute("typ_id",composite_frame)
    dsl_obj = self.create_in_folder(composite_model,"lin_interpol_model.ElmDsl")
    lin_interpol_model = self.get_obj(self.dynamic_model_teamplates_path +
      r"\Linear_interpolation")
    dsl_obj.SetAttribute("typ_id",lin_interpol_model)
    set_dsl_obj_matrix(dsl_obj,points)
    composite_model.SetAttribute("pelm",[dsl_obj])
  
  @staticmethod 
  def set_dsl_obj_matrix(dsl_obj,rows):
    dsl_obj.SetAttribute("matrix:0",[len(rows),0])
    for idx, row in enumerate(rows):
      attrib = "matrix:" + str(idx+1)
      dsl_obj.SetAttribute(attrib,row)

  @staticmethod 
  def get_dsl_obj_matrix(dsl_obj):
    number_of_rows = dsl_obj.GetAttribute("matrix:0")
    matrix = []
    for idx in range(int(number_of_rows[0])):
      attrib = "matrix:" + str(idx+1)
      matrix.append(dsl_obj.GetAttribute(attrib))
    return matrix

class SimulationStudyCases(PFBaseInterface,PFDynSimInterface):

  def __init__(self,app):
    PowerFactoryInterface.__init__(self, app)
    self.name = ""
    self.monitored_variables: dict
    self.parameters: dict
    self.parameter_name_adjustments = {}
    self.parameter_value_adjustments = {}
    self.parameters_ignored_in_iterable = []
    self.simulate_permutations = False

  def get_parameter_values_iterable(self):
    if not self.simulate_permutations:
      return list(map(list, zip(*self.parameters.values())))
    else:
      return itertools.product(*self.parameters.values())
    
  def get_parameters_equals_values_string(self, values):
    param_names_and_values = []
    for idx, param_path in enumerate(self.parameters.keys()):
      values[idx] = self.get_adjusted_parameter_value_string(param_path,values[idx])
      param_name = self.get_adjusted_parameter_name(param_path)
      param_names_and_values.append(param_name+"="+values[idx])
    return '    '.join(param_names_and_values)

  def get_adjusted_parameter_value_string(self,param_path,value):
    value = float(value)
    print(value)
    if param_path in self.parameter_value_adjustments:
        value = value*self.parameter_value_adjustments[param_path]
    if value > 1e3 or value < 1e-2:   
      return str("{:.2E}".format(value))
    else:
      return str("{:.2f}".format(value))

  def get_adjusted_parameter_name(self,param_path):
    if param_path in self.parameter_name_adjustments:
      return self.parameter_name_adjustments[param_path]
    else:
      return os_path.split(param_path)[1]

  def get_parameters_equals_values_string_with_study_case_name(self, values):
    string = self.get_parameters_equals_values_string(values)
    if self.name:
      return self.name + ' ' + string
    else:
      return string

  def import_study_case(self,study_case_data):
    self.parameters = study_case_data["Parameters"]
    self.monitored_variables = study_case_data["Monitored variables"]    

  def simulate_cases(self):  
    simulation_result_names = []
    for case_num, param_values in enumerate(self.get_parameter_values_iterable()):
        for param_num, param_path in enumerate(self.parameters.keys()):
            self.set_attr_by_path(param_path,param_values[param_num])
        param_values = list(param_values) # must be mutable
        simulation_result_name = self.get_parameters_equals_values_string_with_study_case_name(param_values)
        self.results = "case" + str(case_num) + ".ElmRes"
        results_storage_obj = self.app.GetFromStudyCase(self.results)
        self.set_attr(results_storage_obj,{"desc": [simulation_result_name]})
        self.initialize_dyn_sim(param={"p_resvar":results_storage_obj})
        for k,v in self.monitored_variables.items():
          self.add_results_variable(k,v)
        self.sim()
        simulation_result_names.append(simulation_result_name)
    return simulation_result_names