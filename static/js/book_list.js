// View toggle functionality
document.getElementById('gridView').addEventListener('click', function() {
    this.classList.add('active');
    document.getElementById('listView').classList.remove('active');
    document.getElementById('booksContainer').className = 'row';
});

document.getElementById('listView').addEventListener('click', function() {
    this.classList.add('active');
    document.getElementById('gridView').classList.remove('active');
    document.getElementById('booksContainer').className = 'row row-cols-1';
});

// Auto-submit search on enter
document.querySelector('input[name="search"]').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Prevent double submit
        document.getElementById('filterForm').submit();
    }
});

function applyAdvancedFilters() {
    const author = document.getElementById('authorSelect').value;
    const publisher = document.getElementById('publisherSelect').value;
    const year_from = document.getElementById('yearFromSelect').value;
    const year_to = document.getElementById('yearToSelect').value;
    const pages_min = document.querySelector('#advancedFilterForm input[name="pages_min"]').value;
    const pages_max = document.querySelector('#advancedFilterForm input[name="pages_max"]').value;

    // Update hidden fields
    document.querySelector('#filterForm input[name="author"]').value = author;
    document.querySelector('#filterForm input[name="publisher"]').value = publisher;
    document.querySelector('#filterForm input[name="year_from"]').value = year_from;
    document.querySelector('#filterForm input[name="year_to"]').value = year_to;
    document.querySelector('#filterForm input[name="pages_min"]').value = pages_min;
    document.querySelector('#filterForm input[name="pages_max"]').value = pages_max;

    document.getElementById('filterForm').submit();

    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('advanceSearchModal'));
    if (modal) modal.hide();
}

function clearAdvancedFilters() {
    // Clear modal
    document.getElementById('authorSelect').value = '';
    document.getElementById('publisherSelect').value = '';
    document.getElementById('yearFromSelect').value = '';
    document.getElementById('yearToSelect').value = '';
    document.querySelector('#advancedFilterForm input[name="pages_min"]').value = '';
    document.querySelector('#advancedFilterForm input[name="pages_max"]').value = '';

    // Clear hidden fields
    ['author', 'publisher', 'year_from', 'year_to', 'pages_min', 'pages_max'].forEach(name => {
        const el = document.querySelector(`#filterForm input[name="${name}"]`);
        if (el) el.value = '';
    });

    document.getElementById('filterForm').submit();
}

// Initialize modal with current values
document.getElementById('advanceSearchModal').addEventListener('show.bs.modal', function () {
    const mainForm = document.getElementById('filterForm');

    // Sync hidden → modal
    document.getElementById('authorSelect').value = mainForm.querySelector('input[name="author"]').value || '';
    document.getElementById('publisherSelect').value = mainForm.querySelector('input[name="publisher"]').value || '';
    document.getElementById('yearFromSelect').value = mainForm.querySelector('input[name="year_from"]').value || '';
    document.getElementById('yearToSelect').value = mainForm.querySelector('input[name="year_to"]').value || '';
    document.querySelector('#advancedFilterForm input[name="pages_min"]').value = mainForm.querySelector('input[name="pages_min"]').value || '';
    document.querySelector('#advancedFilterForm input[name="pages_max"]').value = mainForm.querySelector('input[name="pages_max"]').value || '';
});