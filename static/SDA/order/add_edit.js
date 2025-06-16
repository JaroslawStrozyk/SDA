function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


$(document).ready(function () {
    // Pobranie wartości pola FL
    var flValue = $('#FL').val();
    var getNipDetailsUrl, addNipUrl;

    // Ustawienie odpowiednich URL na podstawie wartości pola FL
    if (flValue === 'new') {
        getNipDetailsUrl = '/ZAMOWIENIA/ord_new/get_nip_details/';
        addNipUrl = '/ZAMOWIENIA/ord_new/add_nip/';
    } else {
        getNipDetailsUrl = '/ZAMOWIENIA/ord_edit/get_nip_details/';
        addNipUrl = '/ZAMOWIENIA/ord_edit/add_nip/';
    }

    // Obsługa zmiany w form.nip_ind
    $('#id_nip_ind').change(function () {
        var selectedNipInd = $(this).val();

        // Zapytanie AJAX do pobrania informacji na podstawie wybranego nip_ind
        $.ajax({
            url: getNipDetailsUrl,
            data: {
                'nip_ind': selectedNipInd,
            },
            success: function (data) {
                $('#id_nip').val(data.nip);
                $('#id_kontrahent').val(data.kontrahent);
            }
        });
    });

    // Wyświetlenie okna modalnego po kliknięciu przycisku
    $('#nip_add').click(function (e) {
        e.preventDefault();
        $('#addNipModal').modal('show');
    });

    // Obsługa kliknięcia przycisku dodania
    $('#saveNip').click(function () {
        var newNip = $('#newNip').val();
        var newKontrahent = $('#newKontrahent').val();

        $.ajax({
            type: 'POST',
            url: addNipUrl,  // Zakładam, że masz taki endpoint
            headers: { 'X-CSRFToken': csrftoken },
            data: {
                'nip': newNip,
                'kontrahent': newKontrahent  //,
                // 'csrfmiddleware token': $('#id_nip_ind [name="csrfmiddleware token"]').val()  // {% csrf_token %}
            },
            success: function (data) {
                // Aktualizacja pól formularza i dodanie nowego nip_ind
                $('#id_nip').val(newNip);
                $('#id_kontrahent').val(newKontrahent);

                // Możesz także zaktualizować pole form.nip_ind, dodając nową opcję
                $('#id_nip_ind').append(new Option(newNip, data.new_nip_ind, true, true));

                // Zamknięcie okna modalnego
                $('#addNipModal').modal('hide');
            }
        });
    });
});