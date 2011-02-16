# py.test.exe should discover tests autoamically without our help, but I don't
# seem to be able to get it working.
push-location "../tests"
& "py.test.exe"
pop-location