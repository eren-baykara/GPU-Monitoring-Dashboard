Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run chr(34) & "run_gpu_monitor.bat" & Chr(34), 0
Set WshShell = Nothing
