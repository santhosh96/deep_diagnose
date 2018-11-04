function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#blah')
            .attr('src', e.target.result)
            .width(200)
            .height(200);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// $(document).ready(function () {
//     $("#btnSubmit").click(function (event) {
//         //stop submit the form, we will post it manually.
//         event.preventDefault();
//         // Get form
//         var form = $('#fileUploadForm')[0];
//         // Create an FormData object
//         var data = new FormData(form);
//         // If you want to add an extra field for the FormData
//         //data.append("CustomField", "This is some extra data, testing");
//         // disabled the submit button
//         $("#btnSubmit").prop("disabled", true);
//
//         $.ajax({
//             type: "POST",
//             enctype: 'multipart/form-data',
//             url: "http://SEVER_IP OR DAMAIN:PORT/index.html",
//             data: data,
//             processData: false,
//             contentType: false,
//             cache: false,
//             timeout: 600000,
//
//             success: function (data) {
//                 //$("#result").innerHTML(data);
//                 document.getElementById("result").innerHTML = data;
//                 console.log("SUCCESS : ", data);
//                 $("#btnSubmit").prop("disabled", false);
//             },
//
//             error: function (e) {
//                 $("#result").text(e.responseText);
//                 console.log("ERROR : ", e);
//                 $("#btnSubmit").prop("disabled", false);
//             }
//
//         });
//     });
// });
