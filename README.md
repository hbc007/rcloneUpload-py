## rcloneUpload-py
A more reliable file upload tool to upload downloaded files into a remote directory mounted through rclone
## Features
* Move files to the remote directory when download is completed.
* Automatically delete padding files in BT tasks.
* Automatically delete downloaded files when these files are copied correctly into the remote directory, if copy task failed unexpectedly, source files will be kept.
* A log file will be created in the same folder as rcloneUpload after copy task finished.
## How to use (on Linux)
1. Download `rcloneUpload`.  
    Only for linux-amd64 now.
2. Create `config.json` in the same folder as `rcloneUpload`.  
    ```
    {
      "downloadDir":"",
      "mountDir":""
    }
    ```
    `downloadDir` is the directory to store the downloaded file  
    `mountDir` is the remote directory mounted through rclone
3. Edit `~/.aria2/aria2.conf`,add this line  
    `on-download-complete=?`  
    `?` is `rcloneUpload` file path.
4. Restart aria2