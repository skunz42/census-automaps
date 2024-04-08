param (
    [Parameter(Mandatory=$true)]
    [ValidateScript({
        $Components = Get-Content ..\config\names.txt
        if ($_ -in $Components) { return $true }
        throw "Please provide a valid ethnicity"
    })]
    [ArgumentCompleter({
        param($cmd, $param, $wordToComplete)
        [array] $Components = Get-Content ..\config\names.txt
        $Components -like "$wordToComplete*" | ForEach-Object { if ($_ -match " ") { Write-Output `"$_`" } else { Write-Output $_ } }
    })]
    [String]$Ethnicity
)

$Python = "C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

$EthnicityFull = "$Ethnicity alone or in any combination"
& $Python make_layouts.py -e $EthnicityFull