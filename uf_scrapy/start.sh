env | sed 's/^\(.*\)$/export \1/g' > /root/envs.sh
chmod +x /root/envs.sh
cron && tail -f /var/log/cron.log