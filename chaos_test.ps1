Write-Host "Starting Chaos Test"

docker stop node3

Start-Sleep -Seconds 10

docker start node3

Start-Sleep -Seconds 5

docker stop node5

Start-Sleep -Seconds 10

docker start node5

Write-Host "Chaos Test Complete"