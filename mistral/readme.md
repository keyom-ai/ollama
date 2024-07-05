# Mistral Chat Interface Setup

This guide will walk you through setting up a chat interface for the Mistral language model using Ollama, Flask, and NGINX on a Linux server.

## Prerequisites

- A Linux server (Ubuntu 20.04 LTS or later recommended)
- Root or sudo access to the server

## Step 1: Install Required Software

Update your system and install the necessary packages:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip nginx
```

## Step 2: Install Ollama

Install Ollama by following these steps:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

After installation, pull the Mistral model:

```bash
ollama pull mistral
```

## Step 3: Set Up the Python Environment

Create a directory for your project and set up a virtual environment:

```bash
mkdir ~/mistral-chat
cd ~/mistral-chat
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install flask flask-cors gunicorn
```

## Step 4: Create the Application Files

Create `app.py` and `index.html` in the `~/mistral-chat` directory. Copy the contents of these files from the provided sources.

## Step 5: Configure NGINX

Create an NGINX configuration file:

```bash
sudo nano /etc/nginx/sites-available/mistral-chat
```

Add the following configuration (replace `your_domain.com` with your actual domain or server IP):

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        root /home/your_username/mistral-chat;
        index index.html;
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

Enable the site and restart NGINX:

```bash
sudo ln -s /etc/nginx/sites-available/mistral-chat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 6: Set Up Gunicorn

Create a systemd service file for Gunicorn:

```bash
sudo nano /etc/systemd/system/mistral-chat.service
```

Add the following content (replace `your_username` with your actual username):

```ini
[Unit]
Description=Gunicorn instance to serve Mistral chat application
After=network.target

[Service]
User=your_username
Group=www-data
WorkingDirectory=/home/your_username/mistral-chat
Environment="PATH=/home/your_username/mistral-chat/venv/bin"
ExecStart=/home/your_username/mistral-chat/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5001 app:app

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
sudo systemctl start mistral-chat
sudo systemctl enable mistral-chat
```

## Step 7: Firewall Configuration (if applicable)

If you're using UFW (Uncomplicated Firewall), allow HTTP traffic:

```bash
sudo ufw allow 'Nginx Full'
```

## Step 8: Testing the Setup

1. Ensure Ollama is running:
   ```bash
   ollama run mistral "Hello, are you ready?"
   ```

2. Check if the Gunicorn service is running:
   ```bash
   sudo systemctl status mistral-chat
   ```

3. Visit your domain or server IP in a web browser. You should see the chat interface.

## Troubleshooting

- Check NGINX error logs: `sudo tail -f /var/log/nginx/error.log`
- Check application logs: `sudo journalctl -u mistral-chat`
- Ensure proper permissions: The NGINX user (www-data) should have read access to your application directory.

## Security Considerations

- Set up HTTPS using Let's Encrypt for secure communication.
- Implement user authentication if this is to be used in a multi-user environment.
- Regularly update all components (OS, Nginx, Python packages, Ollama) to patch security vulnerabilities.

## Maintenance

- Regularly update Ollama and the Mistral model:
  ```bash
  ollama pull mistral
  ```
- Keep your system and Python packages up to date.

For any issues or improvements, please open an issue in the repository.
