@ECHO OFF
ECHO Executing Python Script by batch
setlocal EnableDelayedExpansion
if not "%1"=="" ( echo Path: %1\Hds9.a2l
        ) else ( echo "NO Argument passed to cmd bat - please indicate the path of A2L file to be refactored."
        )

python a2lrefactor.py -i "%1"\Hds9.a2l -o "%1"\Hds9WP.a2l -d WPxA2L_example.xml -m O

