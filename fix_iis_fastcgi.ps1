# Corriger les variables d'environnement FastCGI pour test_py
$python = "C:\inetpub\wwwroot\test_py\venv\Scripts\python.exe"
$wfastcgi = "C:\inetpub\wwwroot\test_py\venv\Lib\site-packages\wfastcgi.py"
$appcmd = "$env:windir\system32\inetsrv\appcmd.exe"

# Corriger WSGI_HANDLER (sans parenthèses)
& $appcmd set config /section:fastCgi `
  "/[fullPath='$python',arguments='$wfastcgi'].environmentVariables.[name='WSGI_HANDLER'].value:back_django_portfolio_me.wsgi.application"

# Corriger PYTHONPATH
& $appcmd set config /section:fastCgi `
  "/[fullPath='$python',arguments='$wfastcgi'].environmentVariables.[name='PYTHONPATH'].value:C:\inetpub\wwwroot\test_py"

# Corriger DJANGO_SETTINGS_MODULE
& $appcmd set config /section:fastCgi `
  "/[fullPath='$python',arguments='$wfastcgi'].environmentVariables.[name='DJANGO_SETTINGS_MODULE'].value:back_django_portfolio_me.settings"

Write-Host "Done. Run iisreset."
