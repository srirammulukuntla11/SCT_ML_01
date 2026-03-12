// Main JavaScript for House Price Predictor

$(document).ready(function() {
    console.log('House Price Predictor initialized');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Quick select buttons
    $('.quick-select').click(function() {
        var bedrooms = $(this).data('bedrooms');
        var bathrooms = $(this).data('bathrooms');
        var area = $(this).data('area');
        
        $('#bedrooms').val(bedrooms);
        $('#bathrooms').val(bathrooms);
        $('#area').val(area);
        
        // Highlight selected button
        $('.quick-select').removeClass('btn-primary').addClass('btn-outline-secondary');
        $(this).removeClass('btn-outline-secondary').addClass('btn-primary');
    });
    
    // Form validation
    $('#predictionForm').submit(function(e) {
        var bedrooms = $('#bedrooms').val();
        var bathrooms = $('#bathrooms').val();
        var area = $('#area').val();
        var isValid = true;
        var errorMessage = '';
        
        // Validate bedrooms
        if (bedrooms < 1 || bedrooms > 10) {
            isValid = false;
            errorMessage += 'Bedrooms must be between 1 and 10\n';
        }
        
        // Validate bathrooms
        if (bathrooms < 0.5 || bathrooms > 8) {
            isValid = false;
            errorMessage += 'Bathrooms must be between 0.5 and 8\n';
        }
        
        // Validate area
        if (area < 300 || area > 50000) {
            isValid = false;
            errorMessage += 'Area must be between 300 and 50000 sq.ft.\n';
        }
        
        if (!isValid) {
            alert('Please correct the following errors:\n' + errorMessage);
            e.preventDefault();
            return false;
        }
        
        // Show loading state
        $(this).find('button[type="submit"]').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Predicting...').prop('disabled', true);
    });
    
    // Input validation on blur
    $('input[type="number"]').blur(function() {
        validateInput($(this));
    });
    
    // Real-time input formatting
    $('input[type="number"]').on('input', function() {
        var value = $(this).val();
        if (value !== '') {
            // Remove any non-numeric characters except decimal point
            value = value.replace(/[^0-9.]/g, '');
            
            // Ensure only one decimal point
            var parts = value.split('.');
            if (parts.length > 2) {
                value = parts[0] + '.' + parts.slice(1).join('');
            }
            
            $(this).val(value);
        }
    });
    
    // API Test function
    window.testAPI = function() {
        var testData = {
            bedrooms: 3,
            bathrooms: 2,
            area: 1500
        };
        
        $.ajax({
            url: '/api/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(testData),
            success: function(response) {
                console.log('API Response:', response);
                alert('API Test Successful!\nPredicted Price: ' + response.formatted_price);
            },
            error: function(xhr, status, error) {
                console.error('API Error:', error);
                alert('API Test Failed: ' + error);
            }
        });
    };
});

// Input validation function
function validateInput(input) {
    var value = parseFloat(input.val());
    var min = parseFloat(input.attr('min'));
    var max = parseFloat(input.attr('max'));
    var step = parseFloat(input.attr('step')) || 1;
    
    if (isNaN(value)) {
        input.val(min || 0);
        return;
    }
    
    // Round to nearest step
    if (step > 0) {
        value = Math.round(value / step) * step;
    }
    
    // Apply min/max
    if (!isNaN(min) && value < min) {
        value = min;
    }
    if (!isNaN(max) && value > max) {
        value = max;
    }
    
    input.val(value);
}

// Format currency
function formatIndianCurrency(amount) {
    if (amount >= 10000000) {
        return '₹' + (amount / 10000000).toFixed(2) + ' Crore';
    } else if (amount >= 100000) {
        return '₹' + (amount / 100000).toFixed(2) + ' Lakh';
    } else {
        return '₹' + amount.toLocaleString('en-IN');
    }
}

// Show loading spinner
function showLoading() {
    $('#loadingSpinner').removeClass('d-none');
}

// Hide loading spinner
function hideLoading() {
    $('#loadingSpinner').addClass('d-none');
}

// Save prediction to localStorage
function savePrediction(bedrooms, bathrooms, area, price) {
    var predictions = JSON.parse(localStorage.getItem('predictions') || '[]');
    predictions.push({
        bedrooms: bedrooms,
        bathrooms: bathrooms,
        area: area,
        price: price,
        timestamp: new Date().toISOString()
    });
    
    // Keep only last 10 predictions
    if (predictions.length > 10) {
        predictions = predictions.slice(-10);
    }
    
    localStorage.setItem('predictions', JSON.stringify(predictions));
}

// Load predictions from localStorage
function loadPredictions() {
    return JSON.parse(localStorage.getItem('predictions') || '[]');
}

// Clear all predictions
function clearPredictions() {
    if (confirm('Are you sure you want to clear all prediction history?')) {
        localStorage.removeItem('predictions');
        location.reload();
    }
}

// Export predictions as CSV
function exportPredictions() {
    var predictions = loadPredictions();
    if (predictions.length === 0) {
        alert('No predictions to export');
        return;
    }
    
    var csv = 'Bedrooms,Bathrooms,Area (sq.ft.),Price,Timestamp\n';
    predictions.forEach(function(p) {
        csv += `${p.bedrooms},${p.bathrooms},${p.area},"${p.price}",${p.timestamp}\n`;
    });
    
    var blob = new Blob([csv], { type: 'text/csv' });
    var url = window.URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'predictions.csv';
    a.click();
}

// Handle API errors
function handleAPIError(error) {
    console.error('API Error:', error);
    
    var errorMessage = 'An error occurred. Please try again.';
    
    if (error.responseJSON && error.responseJSON.error) {
        errorMessage = error.responseJSON.error;
    } else if (error.status === 500) {
        errorMessage = 'Server error. Please try again later.';
    } else if (error.status === 404) {
        errorMessage = 'API endpoint not found.';
    } else if (error.status === 400) {
        errorMessage = 'Invalid input data.';
    }
    
    alert('Error: ' + errorMessage);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add animation classes
    document.querySelectorAll('.card').forEach(function(card, index) {
        card.style.animation = `fadeIn 0.5s ease-out ${index * 0.1}s both`;
    });
    
    // Check for saved theme preference
    var darkMode = localStorage.getItem('darkMode') === 'true';
    if (darkMode) {
        document.body.classList.add('dark-mode');
    }
});