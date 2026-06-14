let searchTimeout = null;
let searchInput = null;
let suggestionsContainer = null;

document.addEventListener('DOMContentLoaded', function() {
    searchInput = document.querySelector('input[type="search"]');
    if (!searchInput) return;
    
    suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'position-absolute w-100 bg-white shadow rounded mt-1';
    suggestionsContainer.style.zIndex = '1000';
    suggestionsContainer.style.display = 'none';
    searchInput.parentNode.style.position = 'relative';
    searchInput.parentNode.appendChild(suggestionsContainer);
    
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();
        
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }
        
        if (query.length < 2) {
            suggestionsContainer.style.display = 'none';
            return;
        }
        
        searchTimeout = setTimeout(function() {
            fetch('/api/search/?q=' + encodeURIComponent(query))
                .then(function(response) {
                    return response.json();
                })
                .then(function(data) {
                    if (data.suggestions && data.suggestions.length > 0) {
                        var html = '';
                        for (var i = 0; i < data.suggestions.length; i++) {
                            var s = data.suggestions[i];
                            html += '<a href="' + s.url + '" class="text-decoration-none">' +
                                '<div class="p-3 border-bottom" style="cursor: pointer;">' +
                                '<div class="fw-semibold text-dark">' + escapeHtml(s.title) + '</div>' +
                                '</div></a>';
                        }
                        suggestionsContainer.innerHTML = html;
                        suggestionsContainer.style.display = 'block';
                    } else {
                        suggestionsContainer.innerHTML = '<div class="p-3 text-secondary small">No results found</div>';
                        suggestionsContainer.style.display = 'block';
                    }
                })
                .catch(function() {
                    suggestionsContainer.innerHTML = '<div class="p-3 text-danger small">Search error</div>';
                    suggestionsContainer.style.display = 'block';
                });
        }, 300);
    });
    
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.style.display = 'none';
        }
    });
});

function escapeHtml(text) {
    var div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}