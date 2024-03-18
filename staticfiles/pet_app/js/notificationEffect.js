function markAsRead(notificationId) {
    axios.post(`{% url 'userprofile:mark_notification_as_read' 0 %}`.replace('/0/', `/${notificationId}/`), {}, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
        .then(response => {
            if (response.data.status === 'success') {
                document.getElementById(`notification-${notificationId}`).remove();
            }
        })
        .catch(error => console.error('Error marking notification as read:', error));
}


function fetchNotifications() {
    axios.get("{% url 'userprofile:get_notifications' %}")
        .then(response => {
            const notifications = response.data.notifications;
            updateNotificationUI(notifications);
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

function updateNotificationUI(notifications) {
    const notificationList = document.getElementById("notificationList");
    notificationList.innerHTML = ''; // Clear existing notifications

    notifications.forEach(notification => {
        const div = document.createElement('div');
        div.id = `notification-${notification.id}`;
        div.className = 'notification-item';
        div.textContent = notification.message; // Update as needed
        div.onclick = () => markAsRead(notification.id); // Add onclick event
        notificationList.appendChild(div);
    });

    // Update notification count
    const notificationButton = document.getElementById("notificationButton");
    notificationButton.textContent = `Notifications (${notifications.length})`;
}

document.addEventListener('DOMContentLoaded', fetchNotifications)