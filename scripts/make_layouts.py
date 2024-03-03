import argparse
import os
import pathlib
import sys

import arcpy

# Plan:
# Ethnicity as parameter
# Add map if doesn't exist w/ Ethnicity name
# Set map as current map
# Add county and state shapefiles

GDB_PATH = r"C:\census-automaps\GDBs"
PROJECT_PATH = r"C:\census-automaps\ProProjects"
TEMPLATE_PATH = r"C:\census-automaps\ProProjects\Template\Template.aprx"
TOTAL_FC_PATH = r"C:\census-automaps\GDBs\Total.gdb\CountiesTotal"
SDE_PATH = r"C:\census-automaps\SDEs\censusdata.sde"
SDE_TABLE_NAME = "census.public.dmgs"
JOIN_FIELD = "FIPS"
TOTAL_PREFIX = f"{os.path.split(TOTAL_FC_PATH)[-1]}_"


def add_message(text):
    arcpy.AddMessage(text)


def update_map_properties(current_map, ethnicity):
    # create gdb
    gdb_path = os.path.join(GDB_PATH, f"{ethnicity}.gdb")
    if not arcpy.Exists(gdb_path):
        add_message("Creating GDB")
        arcpy.management.CreateFileGDB(GDB_PATH, f"{ethnicity}.gdb")
    else:
        add_message("GDB exists")

    # set workspace
    workspace = os.path.join(GDB_PATH, f"{ethnicity}.gdb")
    add_message(f"Workspace value: {workspace}")
    arcpy.env.workspace = workspace

    # set overwrite to true
    arcpy.env.overwriteOutput = True

    # rename map
    add_message(f"Current name of map: {current_map.name}")
    current_map.name = ethnicity
    add_message(f"Changed name of map: {current_map.name}")


def add_county_totals(current_map):
    # iterate through layers so we're not adding a duplicate layer
    layers = current_map.listLayers()
    layers_strs = set()
    for layer in layers:
        layers_strs.add(layer.name)

    _, total_fc = os.path.split(TOTAL_FC_PATH)

    if total_fc not in layers_strs:
        add_message(f"Adding county total population layer ({total_fc}) to the map")
        current_map.addDataFromPath(TOTAL_FC_PATH)


def add_ethnicity_data(ethnicity):
    data_path = os.path.join(SDE_PATH, SDE_TABLE_NAME)
    table_name = f"{ethnicity}Table"

    expression = "groupid = '1114'"

    add_message(expression)

    # add queried data to gdb table
    arcpy.conversion.ExportTable(data_path, table_name, where_clause=expression)
    add_message(f"Added data from path: {data_path} to the default geodatabase")


def add_join(current_map, ethnicity):
    default_gdb = arcpy.env.workspace
    table_path = f"{default_gdb}\\{ethnicity}Table"
    fc_path = f"{default_gdb}\\{ethnicity}FC"

    # Join fields
    joined_table = arcpy.management.AddJoin(
        TOTAL_FC_PATH, JOIN_FIELD, table_path, JOIN_FIELD
    )
    add_message("Joined data to total feature class")

    # Copy to new fc
    arcpy.management.CopyFeatures(joined_table, fc_path)
    add_message(f"Created feature class: {fc_path}")
    current_map.addDataFromPath(fc_path)

    # Remove unnecessary fields
    for field in arcpy.ListFields(fc_path):
        if field.name.startswith(f"{ethnicity}Table_"):
            if field.name != f"{ethnicity}Table_{ethnicity}":
                add_message(f"Deleting field: {field.name}")
                arcpy.management.DeleteField(fc_path, field.name)
            else:
                add_message(f"Setting field: {field.name} to {ethnicity}")
                arcpy.management.AlterField(fc_path, field.name, ethnicity)
        else:
            add_message(f"Removing prefix from field name for field {field.name}")
            arcpy.management.AlterField(
                fc_path, field.name, field.name[len(TOTAL_PREFIX) :]
            )

    # Set nulls to zeroes
    add_message("Removing nulls")
    arcpy.management.CalculateField(
        fc_path, ethnicity, f"!{ethnicity}! if !{ethnicity}! else 0", "PYTHON3"
    )

    # Add per capita field
    add_message("Creating per capita field")
    arcpy.management.CalculateField(
        fc_path,
        f"Per{ethnicity}",
        f"100 * int(!{ethnicity}!) / !TOTAL!",
        "PYTHON3",
        field_type="FLOAT",
    )


def edit_map_properties(current_map):
    old_sr = current_map.spatialReference.name
    add_message(f"Current spatial reference: {old_sr}")
    new_sr = arcpy.SpatialReference(102008)
    add_message(f"New spatial reference: {new_sr.name}")
    current_map.spatialReference = new_sr


def load_ethnicity_data(ethnicity):
    # Script execution code goes here

    add_message(f"Ethnicity: {ethnicity}")

    aprx = arcpy.mp.ArcGISProject(TEMPLATE_PATH)

    m = aprx.listMaps()[0]
    update_map_properties(m, ethnicity)

    add_county_totals(m)
    add_ethnicity_data(ethnicity)

    # add_join(m, ethnicity)
    # # TODO change symbology
    # edit_map_properties(m)

    # Make ethnicity directory if doesn't exist
    aprx_dir = os.path.join(PROJECT_PATH, ethnicity)
    if not os.path.exists(aprx_dir):
        os.makedirs(aprx_dir)

    # save new aprx
    new_aprx = os.path.join(PROJECT_PATH, ethnicity, f"{ethnicity}.aprx")
    pathlib.Path(new_aprx).unlink(missing_ok=True)  # delete old copy
    aprx.saveACopy(new_aprx)


# This is used to execute code if the file was run but not imported
if __name__ == "__main__":
    # Tool parameter accessed with GetParameter or GetParameterAsText

    # not running as a tool
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            prog="Ancestry Map Generator",
            description="Generates maps for a given ethnicity",
        )
        parser.add_argument("-e", "--ethnicity")

        args = parser.parse_args()

        add_message("Running as a script")

        ethnicity = args.ethnicity
    else:
        add_message("Working as a toolbox")
        ethnicity = arcpy.GetParameterAsText(0)

    load_ethnicity_data(ethnicity)