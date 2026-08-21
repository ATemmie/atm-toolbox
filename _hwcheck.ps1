$cs = Get-CimInstance Win32_ComputerSystem
"Model: $($cs.Manufacturer) $($cs.Model)"
"RAM_GB: $([math]::Round($cs.TotalPhysicalMemory/1GB,0))"
$gpu = Get-CimInstance Win32_VideoController
foreach($g in $gpu){ "GPU: $($g.Name)" }
