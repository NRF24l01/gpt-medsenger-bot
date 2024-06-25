sudo pip3 install -r requirements.txt
sudo cp gpt.ini /etc/uwsgi/apps/
sudo cp agents_gpt.conf /etc/supervisor/conf.d/
sudo cp agents_gpt_nginx.conf /etc/nginx/sites-enabled/
sudo supervisorctl update
sudo systemctl restart nginx
sudo certbot --nginx -d gpt.ai.medsenger.ru
