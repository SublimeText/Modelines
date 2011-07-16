$script:here = split-path $MyInvocation.MyCommand.Definition -parent

push-location "$script:here/.."
	remove-item "*.pyc" -recurse -erroraction silentlycontinue
	remove-item "build" -recurse -erroraction silentlycontinue
	remove-item "dist" -recurse -erroraction silentlycontinue
pop-location
