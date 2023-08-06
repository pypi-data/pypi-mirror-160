from numpy import outer
import arcpy
import os
import Tkinter as tk
from tkinter import messagebox
import tkFileDialog as filedialog
from tkFileDialog import askopenfilename
from simpledbf import Dbf5
import pandas as pd
from os.path import exists

class initiation_process:
    @staticmethod
    def initiate_process():
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("","Please input your crown plot")
        global folder_plot
        folder_plot = filedialog.askdirectory()
        messagebox.showinfo("","Please input your area location")
        global area_location
        area_location = filedialog.askdirectory()
        messagebox.showinfo("","Please input folder to store result")
        global gdb_location
        gdb_location = filedialog.askdirectory()
        root.destroy

class starting_first:
    @staticmethod
    def starting_process():
        global mxd
        mxd = arcpy.mapping.MapDocument("Current")
        mxd.author = "Dwieka"
        arcpy.env.workspace = "CURRENT"
        global df
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        global plotting_data
        plotting_data = []
        global plotting_data_tif
        plotting_data_tif = []
        global plotting_area
        plotting_area = []

        substring_plot = ".shp"
        substring_plot_2 = ".xml"
        substring_plot_3 = "DESKTOP"

        for file in os.listdir(folder_plot):
            if file.find(substring_plot) != -1 and file.find(substring_plot_2) == -1 and file.find(substring_plot_3) == -1:
                base = os.path.splitext(file)[0]

                location_plot = os.path.join(folder_plot,file)
                new_layer = arcpy.mapping.Layer(location_plot)
                arcpy.mapping.AddLayer(df,new_layer,"BOTTOM")

                plotting_data.append(base)
            elif file.endswith('.tif') or file.endswith('.ecw'):
                data_process = os.path.join(folder_plot,file)
                data_show = file
                arcpy.MakeRasterLayer_management(data_process,data_show,"","")
                plotting_data_tif.append(file)

        for area in os.listdir(area_location):
            if area.find(substring_plot) != -1 and area.find(substring_plot_2) == -1 and area.find(substring_plot_3) == -1:
                base = os.path.splitext(area)[0]
                area_plot = os.path.join(area_location,area)
                new_layer = arcpy.mapping.Layer(area_plot)
                arcpy.mapping.AddLayer(df,new_layer,"BOTTOM")
                plotting_area.append(base)

class create_folder:
    def __init__(self,main_location):
        self.main_location = main_location
    
    def create_folder(self):
        outputgdb = "crowndetection.gdb"
        # outputgdbmiddle = "middle.gdb"
        folder_making = ["clip_ileaf","iso_result","leaf","point_process","outer_ring","middle_ring"]

        for folder in folder_making:
            location = os.path.join(self.main_location,folder)
            os.mkdir(location)

        global location_masking
        location_masking = os.path.join(self.main_location,folder_making[0])
        global iso_location
        iso_location = os.path.join(self.main_location,folder_making[1])
        global leaf_location
        leaf_location = os.path.join(self.main_location,folder_making[2])
        global point_process
        point_process = os.path.join(self.main_location,folder_making[3])
        global outer_last_location
        outer_last_location = os.path.join(self.main_location,folder_making[4])
        global middle_ring_location
        middle_ring_location = os.path.join(self.main_location,folder_making[5])
        
        arcpy.CreateFileGDB_management(self.main_location,outputgdb)
        # arcpy.CreateFileGDB_management(middle_ring_location,outputgdbmiddle)

        global loc_gdb
        loc_gdb = os.path.join(self.main_location,outputgdb)
        
class process_shape_first:
    def __init__(self,data_process):
        self.data_process = data_process
        arcpy.Near_analysis(self.data_process,self.data_process,"100 Meters","NO_LOCATION","NO_ANGLE","PLANAR")
        try:
            arcpy.AddField_management(self.data_process,"ket","TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.AddField_management(self.data_process, "buffer", "DOUBLE", "10", "10", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.AddField_management(self.data_process, "fidcopy", "SHORT", "10", "10", "", "", "NULLABLE", "NON_REQUIRED", "")
        except Exception:
            pass

        #Processing Shapefile
        arcpy.CalculateField_management(self.data_process, "ket", "new_class( !NEAR_DIST!)", "PYTHON_9.3", "def new_class(x):\\n    if x <= 6.5:\\n        return \"Very Close\"\\n    elif x > 6.5 and x <= 7.5:\\n        return \"Close\"\\n    elif x >7.5:\\n        return \"Normal\"")

        arcpy.CalculateField_management(self.data_process, "buffer", "[NEAR_DIST] / 1.5", "VB", "")

        arcpy.CalculateField_management(self.data_process, "fidcopy", "autoIncrement()", "PYTHON_9.3", "rec=0 \\ndef autoIncrement(): \\n    global rec \\n    pStart = 1  \\n    pInterval = 1 \\n    if (rec == 0):  \\n        rec = pStart  \\n    else:  \\n        rec += pInterval  \\n    return rec ")

        mylist_dist = list(([float(row.getValue("NEAR_DIST")) for row in arcpy.SearchCursor(self.data_process, fields="NEAR_DIST")]))

        mylist_fid = list(([int(row.getValue("fidcopy")) for row in arcpy.SearchCursor(self.data_process, fields="fidcopy")]))

        ziped = dict(zip(mylist_dist,list(mylist_fid)))

        fids_to_delete = []
        for key, value in ziped.items():
            if float(key) <= 1.0:
                fids_to_delete.append(value)

        if len(fids_to_delete) > 0:
            for fid_to_delete in fids_to_delete:
                arcpy.SelectLayerByAttribute_management(self.data_process,"NEW_SELECTION","\"fidcopy\" = {}".format(fid_to_delete))

                arcpy.DeleteFeatures_management(self.data_process)

            arcpy.Near_analysis(self.data_process,self.data_process,"100 Meters","NO_LOCATION","NO_ANGLE","PLANAR")

            arcpy.CalculateField_management(self.data_process, "ket", "new_class( !NEAR_DIST!)", "PYTHON_9.3", "def new_class(x):\\n    if x <= 6.5:\\n        return \"Very Close\"\\n    elif x > 6.5 and x <= 7.5:\\n        return \"Close\"\\n    elif x >7.5:\\n        return \"Normal\"")

            arcpy.CalculateField_management(self.data_process, "buffer", "[NEAR_DIST] / 1.5", "VB", "")

            arcpy.CalculateField_management(self.data_process, "fidcopy", "[FID]", "VB", "")

class processing_raster:
    def __init__(self, main_location):
        self.main_location = main_location

    def processing_raster(self):
        arcpy.gp.PrincipalComponents_sa(plotting_data_tif[0], os.path.join(self.main_location,"pca"), "4", "")

        arcpy.gp.IsoClusterUnsupervisedClassification_sa("pca","5",os.path.join(iso_location,"iso_flwd"),"5","5","")

class starting_process:
    @staticmethod
    def starting_process():
        location = os.path.expanduser('~/Documents/Avirtech/Avirkey/Avirkey.ini')
        if exists(location):
            initiation_process.initiate_process()

            starting_first.starting_process()

            create_folder(gdb_location).create_folder()

            process_shape_first(data_process=plotting_data[0])

            processing_raster(gdb_location).processing_raster()

class start_outer:
    def __init__(self,main_location):
        self.main_location = main_location
    
    def start_outer(self):
        location_gdb_outer = gdb_location
        global mylist_gridcode
        mylist_gridcode = list(([int(row.getValue("gridcode")) for row in arcpy.SearchCursor(plotting_area[0], fields="gridcode")]))

        for gridcode in mylist_gridcode:
            selection = arcpy.SelectLayerByAttribute_management(plotting_area[0],"NEW_SELECTION","\"gridcode\"={}".format(gridcode))

            arcpy.CopyFeatures_management(selection,os.path.join(location_gdb_outer,"block_{}.shp".format(gridcode)))

            arcpy.SelectLayerByLocation_management(plotting_data[0], "INTERSECT", selection, "", "NEW_SELECTION", "NOT_INVERT")

            arcpy.CopyFeatures_management(plotting_data[0],os.path.join(point_process,"point_{}".format(gridcode)),"0","0","0")

            arcpy.Near_analysis("point_{}".format(gridcode),"point_{}".format(gridcode),"100 Meters","NO_LOCATION","NO_ANGLE","PLANAR")

            arcpy.AddField_management("point_{}".format(gridcode),"bufone","DOUBLE", "10", "10", "", "", "NULLABLE", "NON_REQUIRED", "")

            arcpy.CalculateField_management("point_{}".format(gridcode), "bufone", "[NEAR_DIST] / 3.5", "VB", "")

            arcpy.Buffer_analysis("point_{}".format(gridcode),os.path.join(self.main_location,"buffp_{}".format(gridcode)),"bufone","FULL","ROUND","NONE","","PLANAR")

            arcpy.gp.ExtractByMask_sa("iso_flwd",plotting_area[0],os.path.join(self.main_location,"iso_{}".format(gridcode)))

            arcpy.RasterToPolygon_conversion("iso_{}".format(gridcode),os.path.join(iso_location,"pcartp_{}".format(gridcode)),"SIMPLIFY","VALUE","SINGLE_OUTER_PART","")

            selection_2 = arcpy.SelectLayerByAttribute_management("pcartp_{}".format(gridcode),"NEW_SELECTION","\"gridcode\"={}".format(gridcode))

            arcpy.CopyFeatures_management(selection_2,os.path.join(location_gdb_outer,"leaf_{}.shp".format(gridcode)))

            arcpy.Merge_management("buffp_{};leaf_{}".format(gridcode,gridcode),os.path.join(self.main_location,"merge_{}".format(gridcode)))
            
            try:
                arcpy.AddField_management("merge_{}".format(gridcode),"diss","TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
            except Exception:
                pass

            arcpy.CalculateField_management("merge_{}".format(gridcode),"diss","\"1\"", "VB", "")
            
            arcpy.Dissolve_management("merge_{}".format(gridcode),os.path.join(self.main_location,"diss_{}".format(gridcode)),"diss","","MULTI_PART","DISSOLVE_LINES")

            arcpy.MultipartToSinglepart_management("diss_{}".format(gridcode),os.path.join(self.main_location,"expld_{}".format(gridcode)))

            try:
                arcpy.AddField_management("expld_{}".format(gridcode), "fid_new", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            except Exception:
                pass

            arcpy.CalculateField_management("expld_{}".format(gridcode), "fid_new", "autoIncrement()", "PYTHON_9.3", "rec=0 \\ndef autoIncrement(): \\n    global rec \\n    pStart = 1  \\n    pInterval = 1 \\n    if (rec == 0):  \\n        rec = pStart  \\n    else:  \\n        rec += pInterval  \\n    return rec ")

            gsd_int = float(format(arcpy.Describe(plotting_data_tif[0]).children[0].meanCellHeight, ".2f"))

            arcpy.env.parallelProcessingFactor = "0%"

            arcpy.gp.EucDistance_sa("point_{}".format(gridcode),os.path.join(self.main_location,"euc_{}".format(gridcode)),"",gsd_int,"","PLANAR","","")

            arcpy.gp.ZonalStatistics_sa("expld_{}".format(gridcode),"fid_new","euc_{}".format(gridcode),os.path.join(self.main_location,"zon_{}".format(gridcode)),"MAXIMUM","DATA")

            arcpy.gp.ExtractValuesToPoints_sa("point_{}".format(gridcode),"zon_{}".format(gridcode),os.path.join(self.main_location,"evtp_{}".format(gridcode)),"NONE","VALUE_ONLY")

            arcpy.Buffer_analysis("evtp_{}".format(gridcode),os.path.join(self.main_location,"crown_{}".format(gridcode)),"RASTERVALU","FULL","ROUND","NONE","","PLANAR")

        substring_merge = "crown"
        outer = []
        for merge in arcpy.mapping.ListLayers(mxd):
            if str(merge).find(substring_merge) != -1:
                outer.append(str(merge))
        
        s = ";".join(outer)

        arcpy.Merge_management(s,os.path.join(self.main_location,"outer_ring"))

        arcpy.FeatureClassToFeatureClass_conversion("outer_ring",outer_last_location,"outer_crown_ring")

        try:
            arcpy.AddField_management("outer_crown_ring", "inn", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        except Exception:
            pass

        arcpy.CalculateField_management("outer_crown_ring", "inn", "[RASTERVALU] * 0.25", "VB", "")

class calculate_age:
    def __init__(self,main_location):
        self.main_location = main_location
        for age in arcpy.mapping.ListLayers(mxd):
            if str(age) == "outer_crown_ring":
                try:
                    arcpy.AddField_management("outer_crown_ring", "Shape_area", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

                    arcpy.AddField_management("outer_crown_ring", "jari", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

                    arcpy.AddField_management("outer_crown_ring", "umur", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")
                except Exception:
                    pass

                exp = "!SHAPE.AREA@SQUAREMETERS!"

                arcpy.CalculateField_management("outer_crown_ring", "Shape_area", exp, "PYTHON_9.3")

                arcpy.CalculateField_management("outer_crown_ring", "jari", "Sqr ( [Shape_Area] /(3.14)  )", "VB", "")

                arcpy.CalculateField_management("outer_crown_ring", "umur", "age( !jari!)", "PYTHON", "def age(x):\\n    if x <= 1.5:\\n        return \"<=12 Months\"\\n    elif x > 1.6 and x <= 2:\\n        return \"13 - 24 Months\"\\n    elif x > 2 and x <= 3:\\n        return \"25 - 36 Months\"\\n    elif x > 3 and x <= 4:\\n        return \"37 - 48 Months\"\\n    elif x > 4 and x <= 5:\\n        return \"5 Years\"\\n    elif x > 5 and x <= 5.5:\\n        return \"6 Years\"\\n    elif x > 5.5 and x <= 6:\\n        return \"7 Years\"\\n    elif x > 6:\\n        return \"8 and above years\"")

                arcpy.FeatureToPoint_management("outer_crown_ring", os.path.join(self.main_location,"centroid_outer"), "CENTROID")

                arcpy.FeatureClassToFeatureClass_conversion("centroid_outer",outer_last_location,"centroid_age_outer")

                arcpy.Buffer_analysis("centroid_age_outer",os.path.join(self.main_location,"inner_ring"),"inn","FULL","ROUND","NONE","","PLANAR")

class start_middle:
    def __init__(self,main_location):
        self.main_location = main_location

        substring_crown = "outer_crown_ring"

        for file in arcpy.mapping.ListLayers(mxd):
            if str(file).find(substring_crown) != -1:
                # num_block = str(file).split("_")[1]

                arcpy.Buffer_analysis(file,os.path.join(self.main_location,"buffmid"),"-1 Meters","FULL","ROUND","NONE","","PLANAR")

                arcpy.gp.ExtractByMask_sa(plotting_data_tif[0],"buffmid",os.path.join(self.main_location,"tifmid"))

                arcpy.gp.PrincipalComponents_sa("tifmid", os.path.join(self.main_location,"pcamid"), "4", "")

                arcpy.gp.SegmentMeanShift_sa("pcamid", os.path.join(self.main_location,"sgmntmid"), "20", "20", "5", "")

                arcpy.gp.IsoClusterUnsupervisedClassification_sa("sgmntmid","5",os.path.join(middle_ring_location,"isomid"),"5","5","")

class generate_middle_crown:
    def __init__(self,main_location):
        self.main_location = main_location

    def start_middle(self):
        location_gdb_middle = loc_gdb
        global mylist_mid_gridcode
        mylist_mid_gridcode = list(([int(row.getValue("gridmid")) for row in arcpy.SearchCursor(plotting_area[0], fields="gridmid")]))
        
        for gridmid in mylist_mid_gridcode:
            selection_middle = arcpy.SelectLayerByAttribute_management(plotting_area[0],"NEW_SELECTION","\"gridmid\"={}".format(gridmid))

            # arcpy.CopyFeatures_management(selection_middle,os.path.join(location_gdb_middle,"midd_{}.shp".format(gridmid)))

            arcpy.SelectLayerByLocation_management(plotting_data[0], "INTERSECT", selection_middle, "", "NEW_SELECTION", "NOT_INVERT")

            arcpy.CopyFeatures_management(plotting_data[0],os.path.join(point_process,"poimid_{}".format(gridmid)),"0","0","0")

            arcpy.Buffer_analysis("poimid_{}".format(gridmid),os.path.join(loc_gdb,"bufmid_{}".format(gridmid)),"1 Meters","FULL","ROUND","NONE","","PLANAR")

            arcpy.gp.ExtractByMask_sa("isomid",plotting_area[0],os.path.join(loc_gdb,"imid_{}".format(gridmid)))    
            
            arcpy.RasterToPolygon_conversion("imid_{}".format(gridmid),os.path.join(middle_ring_location,"sgmrtp_{}".format(gridmid)),"SIMPLIFY","VALUE","SINGLE_OUTER_PART","")

            selection_middle_2 = arcpy.SelectLayerByAttribute_management("sgmrtp_{}".format(gridmid),"NEW_SELECTION","\"gridcode\"={}".format(gridmid))

            arcpy.CopyFeatures_management(selection_middle_2,os.path.join(location_gdb_middle,"lmid_{}".format(gridmid)))

            arcpy.Merge_management("bufmid_{};lmid_{}".format(gridmid,gridmid),os.path.join(loc_gdb,"mermid_{}".format(gridmid)))

            try:
                arcpy.AddField_management("mermid_{}".format(gridmid),"diss","TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
            except Exception:
                pass

            arcpy.CalculateField_management("mermid_{}".format(gridmid),"diss","\"1\"", "VB", "")
            
            arcpy.Dissolve_management("mermid_{}".format(gridmid),os.path.join(loc_gdb,"dissmid_{}".format(gridmid)),"diss","","MULTI_PART","DISSOLVE_LINES")

            arcpy.MultipartToSinglepart_management("dissmid_{}".format(gridmid),os.path.join(loc_gdb,"expldmid_{}".format(gridmid)))

            try:
                arcpy.AddField_management("expldmid_{}".format(gridmid), "fid_new", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
            except Exception:
                pass

            arcpy.CalculateField_management("expldmid_{}".format(gridmid), "fid_new", "autoIncrement()", "PYTHON_9.3", "rec=0 \\ndef autoIncrement(): \\n    global rec \\n    pStart = 1  \\n    pInterval = 1 \\n    if (rec == 0):  \\n        rec = pStart  \\n    else:  \\n        rec += pInterval  \\n    return rec ")

            gsd_int_mid = float(format(arcpy.Describe(plotting_data_tif[0]).children[0].meanCellHeight, ".2f"))

            arcpy.env.parallelProcessingFactor = "0%"

            arcpy.gp.EucDistance_sa("poimid_{}".format(gridmid),os.path.join(loc_gdb,"eucmid_{}".format(gridmid)),"",gsd_int_mid,"","PLANAR","","")

            arcpy.gp.ZonalStatistics_sa("expldmid_{}".format(gridmid),"fid_new","eucmid_{}".format(gridmid),os.path.join(loc_gdb,"zonmid_{}".format(gridmid)),"MAXIMUM","DATA")

            arcpy.gp.ExtractValuesToPoints_sa("poimid_{}".format(gridmid),"zonmid_{}".format(gridmid),os.path.join(loc_gdb,"evtpmid_{}".format(gridmid)),"NONE","VALUE_ONLY")

            arcpy.Buffer_analysis("evtpmid_{}".format(gridmid),os.path.join(loc_gdb,"midcrown_{}".format(gridmid)),"RASTERVALU","FULL","ROUND","NONE","","PLANAR")
        
        substring_merge = "midcrown"
        outer_mid = []
        for merge in arcpy.mapping.ListLayers(mxd):
            if str(merge).find(substring_merge) != -1:
                outer_mid.append(str(merge))
        
        s = ";".join(outer_mid)

        arcpy.Merge_management(s,os.path.join(self.main_location,"middle_ring"))

        arcpy.FeatureClassToFeatureClass_conversion("middle_ring",outer_last_location,"middle_crown_ring")

starting_process.starting_process()