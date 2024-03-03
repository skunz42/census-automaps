param (
    [Parameter(Mandatory=$true)]
    [ValidateSet("Albanian")]
    [String]$Ethnicity
)

$Python = "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"
$ScriptName = "make_layouts.py"

& $Python make_layouts.py -e $Ethnicity