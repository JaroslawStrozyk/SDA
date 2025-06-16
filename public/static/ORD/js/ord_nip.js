$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $('meta[name="csrf-token"]').attr('content'));
            }
        }
    });

    function fetchNips() {
        $.ajax({
            url: '/ZAMOWIENIA/nips/list/',
            type: 'GET',
            success: function(nips) {
                $('#nipsTable tbody').empty();
                nips.forEach(function(nip) {
                    $('#nipsTable tbody').append(`
                        <tr>
                            <td style="vertical-align:middle; text-align:center;font-weight:bold;">
                                ${nip.nip}
                            </td>
                            <td style="vertical-align:middle; text-align:center;">
                                ${nip.kontrahent}
                            </td>
                            <td style="vertical-align:middle; text-align:center;">
                                <button class="btn btn-primary edit-btn" data-id="${nip.id}" data-nip="${nip.nip}" data-kontrahent="${nip.kontrahent}">
                                    <i class="fa fa-pencil-square-o" aria-hidden="true"></i>
                                </button>
                                <button class="btn btn-danger delete-btn" data-id="${nip.id}">
                                    <i class="fa fa-trash" aria-hidden="true"></i>
                                </button>
                            </td>
                        </tr>
                    `);
                });
            }
        });
    }
    fetchNips();

    // Obsługa kliknięcia przycisku "Dodaj NIP"
    $('#addNipBtn').on('click', function() {
        var nip = $('#nipInput').val();
        var kontrahent = $('#kontrahentInput').val();
        $.ajax({
            url: '/ZAMOWIENIA/nips/create/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'nip': nip, 'kontrahent': kontrahent }),
            success: function(response) {
                $('#addNipModal').modal('hide');
                fetchNips();

                // Czyszczenie pól formularza w modalu dodawania
                $('#nipInput').val('');
                $('#kontrahentInput').val('');
            }
        });
    });

    // Obsługa kliknięcia przycisku "Edytuj" - otwiera modal z danymi do edycji
    $(document).on('click', '.edit-btn', function() {
        var id = $(this).data('id');
        var nip = $(this).data('nip');
        var kontrahent = $(this).data('kontrahent');
        $('#editIdInput').val(id);
        $('#editNipInput').val(nip);
        $('#editKontrahentInput').val(kontrahent);
        $('#editNipModal').modal('show');
    });

    // Obsługa przycisku "Zapisz zmiany" w modalu edycji
    $('#saveEditBtn').on('click', function() {
        var id = $('#editIdInput').val();
        var nip = $('#editNipInput').val();
        var kontrahent = $('#editKontrahentInput').val();
        $.ajax({
            url: `/ZAMOWIENIA/nips/update/${id}/`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 'nip': nip, 'kontrahent': kontrahent }),
            success: function(response) {
                $('#editNipModal').modal('hide');
                fetchNips();
            }
        });
    });


    $(document).on('click', '.delete-btn', function() {
       var id = $(this).data('id'); // Pobierz ID NIP, który ma zostać usunięty
       // Przekaż ID do przycisku wewnątrz modalu
       $('#deleteNipBtn').data('id', id);
       // Wyświetl modal
       $('#confirmDeleteModal').modal('show');
    });


    $('#deleteNipBtn').on('click', function() {
        var id = $(this).data('id');
        $.ajax({
            url: `/ZAMOWIENIA/nips/delete/${id}/`,
            type: 'DELETE',
            success: function(response) {
                // Zamknij modal po pomyślnym usunięciu
                $('#confirmDeleteModal').modal('hide');
                // Odśwież listę NIP-ów
                fetchNips();
            }
        });
    });
});
