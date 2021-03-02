#!/bin/env pwsh
$pythonversions = @('pypy3','pypy','py','python3','python')
$minimumVersion = '3.7.9'

foreach ($command in $pythonversions) {
    try {
        if(Get-Command -ErrorAction Stop $command){
            $currentver=Invoke-Expression -Command "$command -c 'import platform;print(platform.python_version())'"
            if ($currentver -ge $minimumVersion) {
                Write-Output "Using Python version $currentver ($command)"
                Invoke-Expression "$command pymine"
                exit 0
            }
        }
    }
    Catch {}
}

Write-Output "Couldn't find suitable Python version. Please use your package manager to install Python 3.7.9 or later"
exit 1