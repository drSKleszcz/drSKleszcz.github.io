# Build with the optional portable Ruby environment in this supplied checkout.
# Loading Bundler directly avoids `bundle exec` RUBYOPT quoting failures on paths
# containing spaces. The Linux CI continues to use ordinary `bundle exec`.
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/local-env.ps1"
$env:JEKYLL_ENV = 'production'
ruby -rbundler/setup -e 'load Gem.bin_path("jekyll", "jekyll")' -- build --trace
exit $LASTEXITCODE
