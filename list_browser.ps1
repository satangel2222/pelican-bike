Get-Process | Where-Object {$_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -match 'chrome|edge|firefox|browser'} | Select-Object ProcessName,MainWindowTitle,Id | Format-Table -AutoSize
