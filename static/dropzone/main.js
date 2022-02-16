Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#my-awesome-dropzone",{
    url: "upload/",
    maxFiles: 1,
    maxFilesize: 2,
    acceptedFiles: '.pdf',
    dictDefaultMessage: "<i>Przeciągnij w to miejsce plik źródłowy lub klikając w okno wybierz obiekt z dysku...</i><br><font style='color: red; font-weight: bold;'>Dopuszczalny format pliku to *.pdf<font>"
})
