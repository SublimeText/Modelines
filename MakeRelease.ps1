$zipExe = "$env:ProgramFiles/7-zip/7z.exe"

remove-item "./build" -recurse
new-item -itemtype dir -path "./build" -force > $null

# XXX: Build docs with Sphinx and provide those.
$targetDir = "./build/SublimeModelines.sublime-package"
$out = & $zipExe a "-x!.*" -tzip $targetDir "*.py" "*.txt" "*.rst"

if ($LASTEXITCODE -ne 0) { "7-zip error!"; $out; return }

(resolve-path (join-path `
                    (get-location).providerpath `
                    $targetDir)).path | clip.exe

start-process chrome -arg "https://bitbucket.org/guillermooo/sublimemodelines/downloads"

