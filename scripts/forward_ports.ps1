$wslIp = (wsl hostname -I).Trim().Split(' ')[0]
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=127.0.0.1
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=127.0.0.1 connectport=8000 connectaddress=$wslIp
Write-Host "Forwarded localhost:8000 -> WSL2:$wslIp:8000"
