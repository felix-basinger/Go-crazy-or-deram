document.getElementById('btn-ukraine').addEventListener('click', function() {
    document.getElementById('deliveryOptions').classList.add('d-none');
    document.getElementById('ukraineForm').classList.remove('d-none');
});

document.getElementById('btn-world').addEventListener('click', function() {
    document.getElementById('deliveryOptions').classList.add('d-none');
    document.getElementById('worldForm').classList.remove('d-none');
});

document.getElementById('closeModal').addEventListener('click', function() {
    document.getElementById('orderModal').style.display = 'none';
    document.getElementById('deliveryOptions').classList.remove('d-none');
    document.getElementById('ukraineForm').classList.add('d-none');
    document.getElementById('worldForm').classList.add('d-none');
});

function openOrderModal() {
    document.getElementById('orderModal').style.display = 'flex';
}