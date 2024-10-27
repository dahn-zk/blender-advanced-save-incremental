param (
    [string]$BlenderDirectory = "C:\Program Files\Blender Foundation\Blender 4.2"
)

$BlenderPath = Join-Path -Path $BlenderDirectory -ChildPath "blender.exe"
& $BlenderPath --command extension build `
    --source-dir "../source/advanced_save_incremental" `
    --verbose