import paramiko
import os

# Define SSH parameters
ssh_host = "your_destination_machine_ip"
ssh_port = 22
ssh_username = "your_username"
private_key_path = "/path/to/your/private/key"
remote_backup_command = "/home/pi/oprint/bin/octoprint plugins backup:backup"
remote_backup_dir = "/root/.octoprint/data/backup/"
local_destination_dir = "/path/to/local/destination/dir/"
backup_limit = 7  # maximum number of backups to keep

# Initialize SSH client
ssh_client = paramiko.SSHClient()
ssh_client.load_system_host_keys()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Load your private key
private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

try:
    # Connect to the SSH server using key-based authentication
    ssh_client.connect(ssh_host, ssh_port, ssh_username, pkey=private_key)

    # Execute the backup command
    stdin, stdout, stderr = ssh_client.exec_command(remote_backup_command)

    # Wait for the backup to complete
    stdout.channel.recv_exit_status()

    # List files in the remote backup directory
    remote_backup_files = ssh_client.open_sftp().listdir(remote_backup_dir)

    # Find the newest backup file by sorting based on filename
    newest_backup_file = max(remote_backup_files, key=lambda filename: filename)

    # Define the remote and local paths for SCP
    remote_backup_path = os.path.join(remote_backup_dir, newest_backup_file)
    local_destination_path = os.path.join(local_destination_dir, newest_backup_file)

    # SCP the backup file from the remote machine to the local machine
    scp = ssh_client.open_sftp()
    scp.get(remote_backup_path, local_destination_path)
    scp.close()

    print(f"Backup file downloaded to: {local_destination_path}")

    # List local backup files
    local_backup_files = glob.glob(os.path.join(local_destination_dir, "octoprint-backup-*.zip"))

    # Check if the number of local backup files exceeds the limit
    if len(local_backup_files) > backup_limit:
        # Sort local backup files by modification time (oldest first)
        local_backup_files.sort(key=os.path.getmtime)

        # Calculate the number of files to remove to maintain the limit
        files_to_remove = len(local_backup_files) - backup_limit

        # Remove the oldest backup files
        for i in range(files_to_remove):
            os.remove(local_backup_files[i])
            print(f"Removed old backup file: {local_backup_files[i]}")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the SSH connection
    ssh_client.close()
