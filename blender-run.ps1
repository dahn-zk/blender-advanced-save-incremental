param (
    [string]$BlenderDirectory = "C:\Program Files\Blender Foundation\Blender 4.2"
)

try
{
    $BlenderPath = Join-Path -Path $BlenderDirectory -ChildPath "blender.exe"
    $BlenderProc = Start-Process `
        -FilePath $BlenderPath `
        -ArgumentList "--no-window-focus --open-last --log-level 0 --log-show-timestamp"`
        -PassThru -NoNewWindow
    $script:Proc = $BlenderProc
    Wait-Process -InputObject $BlenderProc
}
finally
{
    $BlenderProc.CloseMainWindow()
}

# to show own blender own logs:
# --log *

# Blender Command Line Arguments https://docs.blender.org/manual/en/4.2/advanced/command_line/arguments.html
# Start-Process https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/start-process
# .CloseMainWindow() https://stackoverflow.com/a/2723188/2601742
# $script:Proc https://stackoverflow.com/a/70510767/2601742
