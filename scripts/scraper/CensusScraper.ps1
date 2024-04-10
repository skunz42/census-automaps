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

$LookupPath = Resolve-Path -Path "../config/name_id_mapping.json"
$Key = Get-Content -Path (Resolve-Path -Path "../config/apikey.txt")

& go build main.go
& ./main -ethnicity `"$Ethnicity`" -lookuppath $LookupPath