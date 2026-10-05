# Optional helper for the portable tools used to build this preview.
$projectRoot = Split-Path $PSScriptRoot -Parent
$rubyBin = Join-Path $projectRoot '.tools/ruby/rubyinstaller-3.3.12-1-x64/bin'
if (Test-Path $rubyBin) {
    $env:PATH = "$rubyBin;C:/Program Files/Git/bin;$env:PATH"
    $env:MSYS2_PATH = Join-Path $projectRoot '.tools/msys64'
    $env:BUNDLE_USER_HOME = Join-Path $projectRoot '.tools/bundler'
    $env:GEM_HOME = Join-Path $projectRoot '.tools/gems'
    $env:GEM_PATH = "$env:GEM_HOME;$projectRoot/.tools/ruby/rubyinstaller-3.3.12-1-x64/lib/ruby/gems/3.3.0"
}
if (Test-Path (Join-Path $projectRoot '.tools/python')) {
    $env:PYTHONPATH = Join-Path $projectRoot '.tools/python'
    $env:PLAYWRIGHT_BROWSERS_PATH = Join-Path $projectRoot '.tools/browsers'
}
