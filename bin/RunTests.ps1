# py.test.exe should discover tests autoamically without our help, but I don't
# seem to be able to get it working.
$script:here = split-path $MyInvocation.MyCommand.Definition -parent
push-location "$script:here/../tests"

& "py.test.exe"
pop-location