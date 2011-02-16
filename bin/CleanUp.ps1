$script:here = split-path $MyInvocation.MyCommand.Definition -parent
push-location "$script:here/.."

remove-item "*.pyc" -recurse
remove-item "build" -recurse

pop-location