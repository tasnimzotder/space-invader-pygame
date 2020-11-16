$rootDir = Get-Location

# setup virtual env and build instaaller
.\venv\Scripts\activate
cmd /c "pyinstaller main.py --onefile --noconsole"

# copy the directories
Copy-Item -Path $rootDir\assets\ -Destination $rootDir\dist -Recurse -Force
Copy-Item -Path $rootDir\data\ -Destination $rootDir\dist -Recurse -Force
Copy-Item -Path $rootDir\fonts\ -Destination $rootDir\dist -Recurse -Force

# remove previous files
try {
    Remove-Item $rootDir\dist\*.7z -Force
    Remove-Item $rootDir\dist\play.exe -Force
}
catch {
    Write-Host "No zip file to remove"
}

Rename-Item -Path $rootDir\dist\main.exe -NewName play.exe


# make archieve
$7zipPath = "$env:ProgramFiles\7-Zip\7z.exe"

Set-Alias 7zip $7zipPath

$Source = "$rootDir\dist\play.exe", "$rootDir\dist\assets", "$rootDir\dist\data", "$rootDir\dist\fonts"
$Target = "$rootDir\dist\dist.7z"

7zip a -mx=9 $Target $Source