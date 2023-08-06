import pandas as pd
import geopandas as gpd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import warnings

from . import helper_funcs
from . import diagnostics

def crosswalk(source_shape_or_filepath, source_shape_id, target_shape_or_filepath, target_shape_id, 
				source_col_id_weights = None, source_col_id_to_be_weighted = None,
				tolerance_percent = 10, tolerance_units = None, 
				export = False, export_filename = None):
	# ------------------------------------additional error handling for columns required


	# ---------------------- read in files
	# rudimentary handling of arguments but suffices for now
	if type(source_shape_or_filepath) == 'str' or isinstance(source_shape_or_filepath, str):
		source_shape = gpd.GeoDataFrame.from_file(source_shape_or_filepath)
	else:
		source_shape = source_shape_or_filepath
	if type(target_shape_or_filepath) == 'str' or isinstance(target_shape_or_filepath, str):
		target_shape = gpd.GeoDataFrame.from_file(target_shape_or_filepath)
	else:
		target_shape = target_shape_or_filepath
	source_shape['area_base_source'] = source_shape.area
	target_shape = target_shape.to_crs(source_shape.crs) # kinda important this one 
	target_shape['area_base_target'] = target_shape.area

	if source_shape_id == target_shape_id:
		shape_id_old = source_shape_id
		source_shape_id = f'source_{source_shape_id}'
		target_shape_id = f'target_{target_shape_id}'
		source_shape.rename(columns={shape_id_old: source_shape_id}, inplace=True)
		target_shape.rename(columns={shape_id_old: target_shape_id}, inplace=True)
		warnings.warn(f'The source_shape_id provided is the same as the target_shape_id (=\'{shape_id_old}\'). These will be renamed to \'{source_shape_id}\' and \'{target_shape_id}\', respectively.')

	# ---------------------------------intersect
	intersect = gpd.overlay(source_shape, target_shape, how='intersection', keep_geom_type=False)
	intersect['intersect_area'] = intersect.area
	# intersect['geom_type'] = intersect['geometry'].geom_type
	intersect['INTERSECT_ID'] = intersect[source_shape_id].astype(str) + '_' + intersect[target_shape_id].astype(str)	

	intersect_unedited = intersect.copy() # preserving just in case - used for user stats below

	# ----------------------------filter intersection based on tolerance
	intersect_smallest_area_from_source_and_target = min(min(intersect['area_base_source']), min(intersect['area_base_target']))

	if tolerance_units is not None and not(np.isnan(tolerance_units)):
		tolerance_percent = (tolerance_units / intersect_smallest_area_from_source_and_target)*100
	elif not(np.isnan(tolerance_percent)):
		tolerance_units = intersect_smallest_area_from_source_and_target*(tolerance_percent/100)
	else:
		raise ToleranceException("Tolerance could not be calculated.")

	intersect_smallest_area_postfilter = tolerance_units
	
	intersect = intersect[intersect['intersect_area'] > intersect_smallest_area_postfilter]

	# ----------------------------add weights and adjust the desired variable, if provided
	
	intersect['weight'] = intersect['intersect_area'] / intersect['area_base_source']
	# intersected['weight'+source_col_id_weights] = intersect['weight']
	if source_col_id_weights is not None:
		# calculate weights-providing variable (e.g. population) by target
		# MUST RAISE ERROR HERE IN CASE SOURCE_COL_ID_WEIGHTS is non-number in excel, e.g. if it has commas as thousands operator, this must raise a proper error
		intersect['intersect_'+source_col_id_weights] = intersect['weight'] * intersect[source_col_id_weights]
		intersect['target_shape_'+source_col_id_weights] = intersect.groupby(target_shape_id)['intersect_'+source_col_id_weights].transform('sum')

		if source_col_id_to_be_weighted is not None:
			intersect['intersect_'+source_col_id_to_be_weighted] = (intersect['weight'] * intersect[source_col_id_to_be_weighted]) * (intersect['intersect_'+source_col_id_weights] / intersect['target_shape_'+source_col_id_weights])
			intersect['target_shape_'+source_col_id_to_be_weighted] = intersect.groupby(target_shape_id)['intersect_'+source_col_id_to_be_weighted].transform('sum')
	
	# ------------------------------get diagnostics
	tolerance_values_sim_prop = [0.00001, 0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.5, 0.9, 1, 1.5]
	if tolerance_percent/100 not in tolerance_values_sim_prop:
		tolerance_values_sim_prop.append(tolerance_percent/100)
		tolerance_values_sim_prop.sort()

	diagnostics_obj = diagnostics.get_diagnostics_obj(source_shape, source_shape_id, target_shape, target_shape_id, intersect_unedited, intersect, tolerance_percent, tolerance_units, tolerance_values_sim_prop)
	
	#-------------------------------------------------------------------------------EXPORT--------------------------
	if export:
		if export_filename is None:
			time_now = datetime.now().strftime('%H%M%S-%Y%m%d')
			filename = 'crosswalk_'+time_now+'.csv'
		else:
			filename = export_filename

		if not(filename.endswith('.csv')):
			filename = filename+'.csv'

		# dropping geometry to save space and time
		intersect.drop('geometry', axis='columns', inplace=False).to_csv(filename, index=False)

	return intersect, diagnostics_obj