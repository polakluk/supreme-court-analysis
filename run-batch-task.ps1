function Get-ScriptDirectory
{
  $Invocation = (Get-Variable MyInvocation -Scope 1).Value
  Split-Path $Invocation.MyCommand.Path
}

$path = Get-ScriptDirectory
$pythonpath = $Home + "\anaconda2\python.exe "

Get-ChildItem -Path $args[0] -Recurse -File -Filter $args[1] |
Foreach-Object {
  Write-Output $_.FullName
}
