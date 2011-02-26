$script:here = split-path $MyInvocation.MyCommand.Definition -parent
push-location "$script:here/.."

& "$script:here/CleanUp.ps1"

$zipExe = "$env:ProgramFiles/7-zip/7z.exe"

& "hg" "update" "release"
$rv = & "hg" "merge" "release" 2>&1

if ($rv.exception -like "*unresolved*") {
	write-host "hg pull --update failed. Take a look." -foreground yellow
	break
}

# remove-item "./build" -recurse -erroraction silentlycontinue
# new-item -itemtype dir -path "./build" -force > $null

# XXX: Build docs with Sphinx and provide those.
$targetDir = "./dist/SublimeModelines.sublime-package"
# $out = & $zipExe a "-x!.*" "-x!_*.txt" -tzip $targetDir "*.py" "*.txt" "*.rst"

# if ($LASTEXITCODE -ne 0) { "7-zip error!"; $out; return }

& "python.exe" ".\setup.py" "spa" "--no-defaults"

(resolve-path (join-path `
                    (get-location).providerpath `
                    $targetDir)).path | clip.exe

start-process chrome -arg "https://bitbucket.org/guillermooo/sublimemodelines/downloads"

& "hg" "update" "default"
pop-location