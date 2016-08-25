function Get-ScriptDirectory
{
  $Invocation = (Get-Variable MyInvocation -Scope 1).Value
  Split-Path $Invocation.MyCommand.Path
}

$modes = 'top-right','bottom-middle'
$path = Get-ScriptDirectory
$pythonpath = $Home + "\anaconda2\python.exe "

foreach( $elem in $modes){
  $current_path = ".\arguments\"
  $current_path += $elem
  Get-ChildItem -Path $current_path -File -Filter *.pdf |
  Foreach-Object {
    Write-Output $_.FullName
    $full_params = $pythonpath + $path +"\politics.py -c pipeline -t all-tasks -m " + $elem + " -f " + $_.FullName
    Invoke-Expression $full_params
  }
}
