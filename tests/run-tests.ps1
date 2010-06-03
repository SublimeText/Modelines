$__old_PYTHONPATH = $env:PYTHONPATH
$env:PYTHONPATH = (resolve-path "..").providerpath

# run tests here
& "./tests.py"

$env:PYTHONPATH = $__old_PYTHONPATH