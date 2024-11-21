function updateNotificationCount() {
    fetch("{% url 'unread_notification_count' %}")
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.notification-icon .badge');
            if (data.unread_count > 0) {
                badge.textContent = data.unread_count;
                badge.style.display = 'inline-block';
            } else {
                badge.style.display = 'none';
            }
        });
}

// Update every 10 seconds
setInterval(updateNotificationCount, 10000);