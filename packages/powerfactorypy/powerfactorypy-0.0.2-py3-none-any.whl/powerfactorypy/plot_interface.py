"""Plotting interface.
"""

import sys
sys.path.insert(0,r'.\src')
import powerfactorypy

class PFPlotInterface(powerfactorypy.PFBaseInterface):

  def __init__(self): 
    self.active_graphics_page = ""
    self.active_plot = ""

  def set_active_graphics_page(self,obj):
    """Accepts a graphics page object or its name."""
    if isinstance(obj, str):
      grb = self.app.GetGraphicsBoard()
      self.active_graphics_page = grb.GetPage(obj,1,"GrpPage")
    else:
      self.active_graphics_page = obj

  def set_active_plot(self,name,graphics_page=None):
    """Accepts the name of the plot."""
    if not graphics_page==None:
      self.set_active_graphics_page(graphics_page)
    self.active_plot = self.active_graphics_page.GetOrInsertCurvePlot(name)

  def add_results_variable(self,obj,variables):
    """
    Adds variables of the object to the PowerFactory results object (ElmRes)
    in self.results. *ToDo: should it really be a string?
    obj: PowerFactory object or its path
    """
    # GetFromStudyCase creates the result file if it doesn't exist
    results_storage_obj = self.app.GetFromStudyCase(self.results)
    obj = self.return_obj_if_path_is_provided(obj)
    if isinstance(variables, str):
      variables = [variables]
    for var in variables:
      results_storage_obj.AddVariable(obj,var)
    results_storage_obj.Load()

  def plot_monitored_variables(self,obj,variables,**kwargs):
    """
    obj: PowerFactory object or its path
    variable: string or list of variable names 
    graphics_page: Name of graphics page
    plot: Name of plot
    """
    if "graphics_page" in kwargs:
      self.set_active_graphics_page(kwargs['graphics_page'])
    if "plot" in kwargs:
      self.set_active_plot(kwargs['plot'])
    data_series = self.active_plot.GetDataSeries()
    if "result_file" in kwargs:
      data_series.SetAttribute("useIndividualResults", 1)
    obj = self.return_obj_if_path_is_provided(obj)
    if isinstance(variables, str):
     variables = [variables]
    for var in variables:
      data_series.AddCurve(obj,var)
      self.set_curve_attributes(data_series,**kwargs)
    self.active_graphics_page.Show()
     
  def plot(self,obj,variables,graphics_page=None,plot=None,**kwargs):
    """
    Plots the variables of 'obj' to the currently active plot.
    Includes adding the variables to the results object.
    The active plot can be set with the conditional arguments.
    """
    obj = self.return_obj_if_path_is_provided(obj)
    self.add_results_variable(obj,variables)
    self.plot_monitored_variables(obj,variables,**kwargs) 
  
  def set_curve_attributes(self,data_series,**kwargs):
    if  "linestyle" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLineStyle")
      list_curveTableAttr[-1] = kwargs['linestyle']
      data_series.SetAttribute("curveTableLineStyle",list_curveTableAttr)
    if "linewidth" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
      list_curveTableAttr[-1] = kwargs['linewidth']
      data_series.SetAttribute("curveTableLineWidth",list_curveTableAttr)
    else:
      # The linewidth must be set to the standard value. Otherwise PF uses 
      # the value from the previous data series (this seems to be a PF bug).
      list_curveTableAttr = data_series.GetAttribute("curveTableLineWidth")
      list_curveTableAttr[-1] = 100
      data_series.SetAttribute("curveTableLineWidth",list_curveTableAttr)
    if "color" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableColor")
      list_curveTableAttr[-1] = kwargs['color']
      data_series.SetAttribute("curveTableColor",list_curveTableAttr)
    # The label must be handled differently because PF returns an empty list
    # if there haven't been any labels specified yet for any of the curves.
    if "label" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableLabel")
      if list_curveTableAttr:
        list_curveTableAttr[-1] = kwargs['label']
      else:
        list_curveTableAttr = [kwargs['label']]
      data_series.SetAttribute("curveTableLabel",list_curveTableAttr)
    if "result_file" in kwargs:
      list_curveTableAttr = data_series.GetAttribute("curveTableResultFile")
      list_curveTableAttr[-1] = self.app.GetFromStudyCase(kwargs['result_file'] + ".ElmRes")
      data_series.SetAttribute("curveTableResultFile",list_curveTableAttr)

  def autoscale(self):
    self.active_graphics_page.DoAutoScale()

  def clear_all_graphics_pages(self):
    """
    Deletes all graphics pages from the graphics board of 
    the active study case. 
    """
    grb = self.app.GetGraphicsBoard()
    graphics = grb.GetContents()
    for graphic in graphics:
      if graphic.GetClassName() == "GrpPage":    
        graphic.RemovePage()
        
  def clear_curves_from_all_plots(self): 
    """
    Clears data (i.e. curves) from all plots of the active study case.
    """     
    grb = self.app.GetGraphicsBoard()
    graphics = grb.GetContents()
    for graphic in graphics:
      if graphic.GetClassName() == "GrpPage":    
        for child in graphic.GetContents(): 
          if child.GetClassName() == "PltLinebarplot":
            data_series =child.GetDataSeries()
            data_series.ClearCurves()
          