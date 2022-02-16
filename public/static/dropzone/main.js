Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#my-awesome-dropzone",{
    url: "upload/",
    maxFiles: 1,
    maxFilesize: 2,
    acceptedFiles: '.pdf',
    dictDefaultMessage: "<i>Przeciągnij w to miejsce plik źródłowy lub klikając w okno wybierz obiekt z dysku...</i><br> Dopuszczalne formaty plików to *.pdf"
})
