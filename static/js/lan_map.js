$(document).ready(function(){

    if($('#result') != null){
        Read();
    }

    $('#create').on('click', function(){
        $ip    = $('#ip').val();
        $nazwa = $('#nazwa').val();
        $typ   = $('#typ').val();
        $opis  = $('#opis').val();
        $uwagi = $('#uwagi').val();


        if($ip == ""){
            alert("Uzupełnij wymagane pola !!!");
        }else{
            $.ajax({
                url: 'create/',
                type: 'POST',
                data: {
                    ip: $ip,
                    nazwa: $nazwa,
                    typ: $typ,
                    opis: $opis,
                    uwagi: $uwagi,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(){
                    Read();
                    $('#ip').val('');
                    $('#nazwa').val('');
                    $('#typ').val('');
                    $('#opis').val('');
                    $('#uwagi').val('');
                }
            });

//            $('form#addUser').trigger("reset");
            $('#myModalN').modal('hide');
        }
    });

    $(document).on('click', '.edit', function(){
        $id = $(this).attr('name');
        window.location = "edit/" + $id;
    });

    $('#update').on('click', function(){
        $ip    = $('#ip').val();
        $nazwa = $('#nazwa').val();
        $typ   = $('#typ').val();
        $opis  = $('#opis').val();
        $uwagi = $('#uwagi').val();

        if($ip == "" || $nazwa == "" || $typ == "" || $opis == "" || $uwagi == ""){
            alert("Uzupełnij wymagane pola !!!");
        }else{
            $id = $('#member_id').val();
            $.ajax({
                url: 'update/' + $id,
                type: 'POST',
                data: {
                    ip: $ip,
                    nazwa: $nazwa,
                    typ: $typ,
                    opis: $opis,
                    uwagi: $uwagi,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function(){
                    window.location = '/';
                }
            });
        }

    });

    $(document).on('click', '.delete', function(){
        $id = $(this).attr('name');
        $.ajax({
            url: 'delete/' + $id,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(){
                Read();
            }
        });
    });
});

function Read(){
    $.ajax({
        url: 'read/',
        type: 'POST',
        async: false,
        data:{
            res: 1,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response){
            $('#result').html(response);
        }
    });
}