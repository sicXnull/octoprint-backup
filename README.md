
# Octoprint Backup

SSH into Octoprint Machine, creates backup & sends to local directory of your choosing. Easy to run via cronjob weekly/monthly/etc




## Deployment

To deploy this project modify the following:

```bash
ssh_host = "your_destination_machine_ip"
ssh_port = 22
ssh_username = "your_username"
private_key_path = "/path/to/your/private/key"
remote_backup_command = "/home/pi/oprint/bin/octoprint plugins backup:backup"
remote_backup_dir = "/root/.octoprint/data/backup/"
local_destination_dir = "/path/to/local/destination/dir/"
backup_limit = 7  # maximum number of backups to keep
```

After completing, run the script

```python3 octoprint.py```

Cronjob example - Sundays @ 12:05pm

```5 12 * * 0 python3 /opt/scripts/octoprint.py```


