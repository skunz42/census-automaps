param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("Albanian")]
    [String]$Ethnicity
)

$Python = "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

& $Python make_layouts.py -e $Ethnicity