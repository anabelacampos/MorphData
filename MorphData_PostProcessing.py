# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 11:51:05 2021

@author: brunofmf
"""
from tkinter.filedialog import askdirectory
import pandas as pd
import math
import os


"""
Load Data from Directory and tag with animals characteristics
"""
def loadSkeletonData(directory):
    dataframe_results = {}
    dataframe_branch_info = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".csv") and "final_results" not in file:
                df = pd.read_csv(root+"\\"+file)
                if "Branch" in file:
                    file_split = file.split("__")
                    df["animal"] = file_split[0]
                    microglia = file[:-23]
                    microglia = microglia.replace("__", "_")
                    df["microglia"] = microglia
                    dataframe_branch_info[file] = df
                else:
                    df.rename(columns={ df.columns[0]: "idx" }, inplace = True)
                    dataframe_results[file] = df
    return dataframe_results, dataframe_branch_info


def loadFractalData(directory):
    dict_box_count = {}
    dict_hull_circle = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if "Hull and Circle Results" in file or "Box Count Summary" in file:
                df = pd.read_csv(root+"\\"+file, sep="	", decimal=',')
                if "Area" in root:
                    area_or_perimeter = "Area"
                else:
                    area_or_perimeter = "Perimeter"
                if "Box Count" in file:
                    #we only want Box Count for outlined images
                    if "Perimeter" in area_or_perimeter:
                        df = removeColumns(df, "Box", area_or_perimeter)
                        dict_box_count[area_or_perimeter] = df
                else:
                    df = removeColumns(df, "Hull", area_or_perimeter)
                    dict_hull_circle[area_or_perimeter] = df
    return dict_box_count, dict_hull_circle


"""
From Dict to one Dataframe with everything as rows
"""
def dictToDf(dictionary):
    for index, key in enumerate(dictionary):
        if index == 0:
            df = pd.DataFrame(dictionary[key])
        else:
            df = df.append(dictionary[key])
    return df


"""
Clean unwated columns
"""
def removeColumns(df, box_or_hull, area_or_perimeter):
    df_aux = pd.DataFrame()
    #handling microglia and animal ids
    df_aux["animal_aux"] = df.iloc[:, 0].str.split("__")
    df_aux["animal"] = df_aux["animal_aux"].apply(lambda x: x[0])
    df_aux["microglia"] = df_aux["animal"] + '_' + df_aux["animal_aux"].apply(lambda x: x[1])
    df_aux["microglia_aux"] = df_aux["microglia"].str.split("_"+area_or_perimeter.upper())
    df_aux["microglia"] = df_aux["microglia_aux"].apply(lambda x: x[0])
    df_aux.drop(columns=['animal_aux'], inplace=True)   
    df_aux.drop(columns=['microglia_aux'], inplace=True)    
    #if box or hull
    if "Box" in box_or_hull:
        #we only want: Fractal Dimension (6); Lacunatory (87)
        df_aux["fractal_dimension"] = df.iloc[:, 5]
        df_aux["lacunarity"] = df.iloc[:, 86]
    else:
        if "Area" in area_or_perimeter:      
            #we only want: shape - Mean Fg
            df_aux["shape_mean_fg"] = df.iloc[:, 1]
        else:
            #we want this
            df_aux["outline_mean_fg"] = df.iloc[:, 1]
            df_aux["density"] = df.iloc[:, 3]
            df_aux["span_ratio_major_minor"] = df.iloc[:, 4]
            df_aux["convex_hull_area"] = df.iloc[:, 7]
            df_aux["convex_hull_perimeter"] = df.iloc[:, 8]
            df_aux["convex_hull_circularity"] = df.iloc[:, 9]
            df_aux["diameter_bounding_circle"] = df.iloc[:, 17]
            df_aux["mean_radius"] = df.iloc[:, 15]
            df_aux["max_span_across_convex_hull"] = df.iloc[:, 6]
            df_aux["max_min_radii"] = df.iloc[:, 13]
    return df_aux


"""
Create new features: Pixel Area (micron 2), Cell area, 1 Pixel Side (micron), Cell perimeter, Roughness, Cell Circularity
"""
def calculateNewColumns(dict_box_count, dict_hull_circle, x, y):                
    #first join all data
    df_hull_circle = dict_hull_circle["Perimeter"].join(dict_hull_circle["Area"].set_index(['microglia','animal']), on=['microglia','animal'])
    df_fractal_data = dict_box_count["Perimeter"].join(df_hull_circle.set_index(['microglia','animal']), on=['microglia','animal'])
    #add new columns
    df_fractal_data["1_pixel_side_micron"] = x/y
    df_fractal_data["1_pixel_area_micron_sq"] = df_fractal_data["1_pixel_side_micron"]**2
    df_fractal_data["cell_area"] = df_fractal_data["1_pixel_area_micron_sq"]*df_fractal_data["shape_mean_fg"]
    df_fractal_data["cell_perimeter"] = df_fractal_data["1_pixel_side_micron"]*df_fractal_data["outline_mean_fg"]
    df_fractal_data["roughness"] = df_fractal_data["cell_perimeter"]/df_fractal_data["convex_hull_perimeter"]
    df_fractal_data["cell_circularity"] = (4*math.pi*df_fractal_data["cell_area"])/(df_fractal_data["cell_perimeter"]*df_fractal_data["cell_perimeter"])
    return df_fractal_data


"""
Save df as csv
"""
def toCsv(df, directory):
    df.to_csv(directory)


"""
MAIN
"""
def __main__():
    ###
    # First Skeleton Data
    ###
    path = askdirectory(title='Where is the folder containing the animals?')
    dict_skeleton_results, dict_branch_info = loadSkeletonData(path)
    #dicts to dataframes if has data
    if(bool(dict_skeleton_results)):
        df_skeleton_results = dictToDf(dict_skeleton_results)
        df_branch_info = dictToDf(dict_branch_info)
        #store csvs
        toCsv(df_skeleton_results, path + os.path.sep + "skeleton_final_results.csv")
        toCsv(df_branch_info, path + os.path.sep + "branch_info_final_results.csv")
    else:
        print("No skeleton data to analyze. Check folder.") 
    ###
    # Then Fractal Data
    ###
    fractal_path = path + os.path.sep + 'FracLac Results'
    #join data
    dict_box_count, dict_hull_circle = loadFractalData(fractal_path)
    if(bool(dict_hull_circle)):
        df_fractal_data = calculateNewColumns(dict_box_count, dict_hull_circle, x=180, y=296)
        #store csv
        toCsv(df_fractal_data, path + os.path.sep + "fraclac_final_results.csv")
    else:
        print("No fractal data to analyze. Check folder.")


__main__()