Write-Host "Peekaboe!"
$files = Get-ChildItem( '*.py' )
foreach ($file in $files ) 
{
  Write-Host  $f 
}

#python -m mpy_cross ili934xnew.py -march=xtensawin -X emit=native