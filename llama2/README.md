# LLaMA Chat Interface Setup

This guide walks you through setting up a chat interface for the LLaMA language model using Ollama, Flask, and NGINX on a Linux server (specifically tested on Amazon EC2 with Amazon Linux 2).

## Prerequisites

- A Linux server (Amazon EC2 instance with Amazon Linux 2 recommended)
- Root or sudo access to the server

## Step 1: Install Required Software

Update your system and install the necessary packages:

```bash
sudo yum update -y
sudo yum install -y python3 python3-pip nginx
```

## Step 2: Install Ollama

Install Ollama by following these steps:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

After installation, pull the LLaMA model:

```bash
ollama pull llama2
```

Verify the installation:

```bash
which ollama
ollama run llama2 "Hello, are you working?"
```

## Step 3: Set Up the Python Environment

Create a directory for your project and set up a virtual environment:

```bash
mkdir ~/llama-chat
cd ~/llama-chat
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install flask flask-cors gunicorn
```

## Step 4: Create the Application Files

Create `app.py` and `index.html` in the `~/llama-chat` directory. Copy the contents of these files from the provided LLaMA-specific sources.

## Step 5: Configure NGINX

Create an NGINX configuration file:

```bash
sudo nano /etc/nginx/conf.d/llama-chat.conf
```

Add the following configuration:

```nginx
server {
    listen 80;
    server_name _;

    root /home/ec2-user/llama-chat;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /generate {
        proxy_pass http://127.0.0.1:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Test the NGINX configuration:

```bash
sudo nginx -t
```

If the test is successful, restart NGINX:

```bash
sudo systemctl restart nginx
```

## Step 6: Set Up Gunicorn

Create a systemd service file for Gunicorn:

```bash
sudo nano /etc/systemd/system/llama-chat.service
```

Add the following content:

```ini
[Unit]
Description=Gunicorn instance to serve LLaMA chat application
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/llama-chat
Environment="PATH=/home/ec2-user/llama-chat/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/ec2-user/llama-chat/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5001 app:app

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start llama-chat
sudo systemctl enable llama-chat
```

## Step 7: Set Correct Permissions

Ensure NGINX has access to your application directory:

```bash
sudo chmod 755 /home/ec2-user
sudo chmod -R 755 /home/ec2-user/llama-chat
```

## Step 8: Firewall Configuration (if applicable)

If you're using the AWS EC2 instance, make sure to open port 80 in your security group settings.

## Step 9: Testing the Setup

1. Ensure Ollama is running:
   ```bash
   ollama run llama2 "Hello, are you ready?"
   ```

2. Check if the Gunicorn service is running:
   ```bash
   sudo systemctl status llama-chat
   ```

3. Visit your server's public IP or domain in a web browser. You should see the LLaMA chat interface.

## Troubleshooting

If you encounter issues, follow these steps:

1. Check NGINX error logs:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```

2. Check application logs:
   ```bash
   sudo journalctl -u llama-chat
   ```

3. If you see permission errors, ensure the correct permissions are set:
   ```bash
   sudo chmod 755 /home/ec2-user
   sudo chmod -R 755 /home/ec2-user/llama-chat
   ```

4. If Ollama is not found, make sure it's in the PATH:
   ```bash
   which ollama
   ```
   Update the `llama-chat.service` file with the correct PATH if necessary.

5. Verify that the LLaMA model is downloaded:
   ```bash
   ollama list
   ```

6. If changes are made to the Flask app, remember to restart the Gunicorn service:
   ```bash
   sudo systemctl restart llama-chat
   ```

## Security Considerations

- Set up HTTPS using Let's Encrypt for secure communication.
- Implement user authentication if this is to be used in a multi-user environment.
- Regularly update all components (OS, Nginx, Python packages, Ollama) to patch security vulnerabilities.

## Maintenance

- Regularly update Ollama and the LLaMA model:
  ```bash
  ollama pull llama2
  ```
- Keep your system and Python packages up to date.

For any issues or improvements, please open an issue in the repository.
