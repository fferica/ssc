// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const searchTypeSelect = document.getElementById('search_type');
    const scadutiFilters = document.getElementById('scaduti-filters');

    // Toggle filter visibility based on search type
    function toggleFilters() {
        scadutiFilters.style.display = (searchTypeSelect.value === 'scaduti') ? 'block' : 'none';
    }

    // Set up event listener
    searchTypeSelect.addEventListener('change', toggleFilters);

    // Initialize on page load
    toggleFilters();
});