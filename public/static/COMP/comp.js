$(document).ready(function() {
    $('.multi-info').tooltip({
        items: ".multi-info",
        content: "Ładowanie danych...",
        position: {
            collision: "flipfit"
        },
        open: function(event, ui) {
            var multiId = $(this).data('id');
            if (multiId) {
                $.ajax({
                    url: '/COMP/ewu/get_multi_usage_details/',  // Upewnij się, że ścieżka jest poprawna
                    type: 'GET',
                    data: { 'mltid': multiId },  // Poprawka nazwy parametru
                    success: function(data) {
                        // Bezpośrednie przypisanie odpowiedzi do tooltipa
                        ui.tooltip.html(data);
                    },
                    error: function(xhr, status, error) {
                        console.error("AJAX error: Status -", status, "Error -", error);
                        ui.tooltip.html('Błąd ładowania danych.');
                    }
                });
            }
        }
    });
});