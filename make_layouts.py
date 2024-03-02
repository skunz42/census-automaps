import os

import arcpy

# Plan:
# Ethnicity as parameter
# Add map if doesn't exist w/ Ethnicity name
# Set map as current map
# Add county and state shapefiles

TOTAL_FC_PATH = r"C:\Users\skunz\Documents\Mapping\Total Pop\Total.gdb\CountiesTotal"
CSV_PATHS = r"C:\Users\skunz\Documents\Mapping\Demographics"
JOIN_FIELD = "FIPS"
TOTAL_PREFIX = f"{os.path.split(TOTAL_FC_PATH)[-1]}_"


def change_map_name(current_map, ethnicity):
    arcpy.AddMessage(f"Name of map: {current_map.name}")
    current_map.name = ethnicity
    arcpy.AddMessage(f"Changed name of map: {current_map.name}")


def add_county_totals(current_map):
    layers = current_map.listLayers()
    layers_strs = set()
    arcpy.AddMessage("Printing layers")
    for layer in layers:
        arcpy.AddMessage(f"Layer: {layer.name}")
        layers_strs.add(layer.name)

    _, total_fc = os.path.split(TOTAL_FC_PATH)

    if total_fc not in layers_strs:
        arcpy.AddMessage(
            f"Adding county total population layer ({total_fc}) to the map"
        )
        current_map.addDataFromPath(TOTAL_FC_PATH)


def add_csv_data(ethnicity):
    csv_file = f"{CSV_PATHS}\\{ethnicity}.csv"
    default_gdb = arcpy.env.workspace
    table_name = f"{ethnicity}Table"

    arcpy.conversion.TableToTable(csv_file, default_gdb, table_name)
    arcpy.AddMessage(f"Added CSV from path: {csv_file} to the default geodatabase")


def add_join(current_map, ethnicity):
    default_gdb = arcpy.env.workspace
    table_path = f"{default_gdb}\\{ethnicity}Table"
    fc_path = f"{default_gdb}\\{ethnicity}FC"

    # Join fields
    joined_table = arcpy.management.AddJoin(
        TOTAL_FC_PATH, JOIN_FIELD, table_path, JOIN_FIELD
    )
    arcpy.AddMessage("Joined data to total feature class")

    # Copy to new fc
    arcpy.management.CopyFeatures(joined_table, fc_path)
    arcpy.AddMessage(f"Created feature class: {fc_path}")
    current_map.addDataFromPath(fc_path)

    # Remove unnecessary fields
    for field in arcpy.ListFields(fc_path):
        if field.name.startswith(f"{ethnicity}Table_"):
            if field.name != f"{ethnicity}Table_{ethnicity}":
                arcpy.AddMessage(f"Deleting field: {field.name}")
                arcpy.management.DeleteField(fc_path, field.name)
            else:
                arcpy.AddMessage(f"Setting field: {field.name} to {ethnicity}")
                arcpy.management.AlterField(fc_path, field.name, ethnicity)
        else:
            arcpy.AddMessage(f"Removing prefix from field name for field {field.name}")
            arcpy.management.AlterField(
                fc_path, field.name, field.name[len(TOTAL_PREFIX) :]
            )

    # Set nulls to zeroes
    arcpy.AddMessage("Removing nulls")
    arcpy.management.CalculateField(
        fc_path, ethnicity, f"!{ethnicity}! if !{ethnicity}! else 0", "PYTHON3"
    )

    # Add per capita field
    arcpy.AddMessage("Creating per capita field")
    arcpy.management.CalculateField(
        fc_path,
        f"Per{ethnicity}",
        f"100 * int(!{ethnicity}!) / !TOTAL!",
        "PYTHON3",
        field_type="FLOAT",
    )


def edit_map_properties(current_map):
    old_sr = current_map.spatialReference.name
    arcpy.AddMessage(f"Current spatial reference: {old_sr}")
    new_sr = arcpy.SpatialReference(102008)
    arcpy.AddMessage(f"New spatial reference: {new_sr.name}")
    current_map.spatialReference = new_sr


def load_ethnicity_data(ethnicity):
    # Script execution code goes here

    arcpy.AddMessage(f"Ethnicity we are mapping: {ethnicity}")

    aprx = arcpy.mp.ArcGISProject("CURRENT")

    m = aprx.listMaps()[0]
    change_map_name(m, ethnicity)
    add_county_totals(m)
    add_csv_data(ethnicity)
    add_join(m, ethnicity)
    # TODO change symbology
    edit_map_properties(m)


# This is used to execute code if the file was run but not imported
if __name__ == "__main__":
    # Tool parameter accessed with GetParameter or GetParameterAsText
    ethnicity = arcpy.GetParameterAsText(0)

    load_ethnicity_data(ethnicity)

