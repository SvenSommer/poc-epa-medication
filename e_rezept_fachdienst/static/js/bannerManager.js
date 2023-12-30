// Function to show banner

export function showBanner(message, type) {
    let banner = `<div class="alert ${type === 'success' ? 'alert-success' : 'alert-danger'}">${message}</div>`;
    $('#banner').html(banner);
    setTimeout(() => $('#banner').html(''), 7000); // Banner will disappear after 3 seconds
}
