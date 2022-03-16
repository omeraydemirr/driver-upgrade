$(document).ready(function () {


    $('#csvButton').on("click", function (event) {
        $("#driverForm").hide();
        $(this).hide();
        $("#csvForm").show();
        $("#formButton").show();
        $("#sendButton").hide();
        $("#uploadButton").show();

    })
    $('#formButton').on("click", function (event) {
        $("#driverForm").show();
        $(this).hide();
        $("#csvForm").hide();
        $("#csvButton").show();
        $("#uploadButton").hide();
        $("#sendButton").show();

    })


   


    $('#uploadButton').on("click", function (event) {
        var data = new FormData($('#csvForm').get(0));
        data.append("file", $("#id_file")[0].files);
        $.ajax({
            type: "POST",
            url: "driver",
            data: data,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': "{{ csrf_token }}"
            },

            success: function () {
                alert("successs")
            },
            error: function () {

            }
        })

    })

    $("#vendorSelectValue").change(function (e) {
        e.preventDefault();
        var select = document.getElementById("deviceSelectValue");
        var length = select.options.length;
        for (i = length - 1; i >= 1; i--) {
            select.options[i] = null;
        }
        var select1 = document.getElementById("modelSelectValue");
        var length1 = select1.options.length1;
        for (i = length1 - 1; i >= 1; i--) {
            select1.options[i] = null;
        }
        var select2 = document.getElementById("osSelectValue");
        var length2 = select2.options.length2;
        for (i = length2 - 1; i >= 1; i--) {
            select2.options[i] = null;
        }

        var select3 = document.getElementById("seriesSelectValue");
        var length3 = select.options.length3;
        for (i = length3 - 1; i >= 1; i--) {
            select3.options[i] = null;
        }

        let vendor = $(this).val();
        $.ajax({
            type: 'GET',
            url: "items",
            data: { vendor: vendor, option: 'vendor' },
            headers: {
                'X-CSRFToken': "{{ csrf_token }}",
            },

            success: function (response) {
                hwJson = {};
                hwArray = [];
                for (hwItem of response.devices) {
                    hwJson[hwItem] = hwItem;
                    hwArray.push(hwItem);
                }
                var sel = document.getElementById('deviceSelectValue');
                for (var i = 0; i < hwArray.length; i++) {
                    var opt = document.createElement('option');
                    opt.innerHTML = hwArray[i];
                    opt.value = hwArray[i];
                    sel.appendChild(opt);
                }
            }

        })
    })


    $("#deviceSelectValue").change(function (e) {
        e.preventDefault();
        var select = document.getElementById("modelSelectValue");
        var length = select.options.length;
        for (i = length - 1; i >= 1; i--) {
            select.options[i] = null;
        }

        var select = document.getElementById("osSelectValue");
        var length = select.options.length;
        for (i = length - 1; i >= 1; i--) {
            select.options[i] = null;
        }


        var select = document.getElementById("seriesSelectValue");
        var length = select.options.length;
        for (i = length - 1; i >= 1; i--) {
            select.options[i] = null;
        }


        let device = $(this).val();
        let vendor = $('#vendorSelectValue').val()
        $.ajax({
            type: 'GET',
            url: "items",
            data: { device: device, vendor: vendor, option: 'device' },
            headers: {
                'X-CSRFToken': "{{ csrf_token }}",
            },

            success: function (response) {

                modelJson = {};
                modelArray = [];
                for (modelItem of response.models) {
                    modelJson[modelItem] = modelItem;
                    modelArray.push(modelItem);
                }
                var sel = document.getElementById('modelSelectValue');
                for (var i = 0; i < modelArray.length; i++) {
                    var opt = document.createElement('option');
                    opt.innerHTML = modelArray[i];
                    opt.value = modelArray[i];
                    sel.appendChild(opt);
                }
            }

        })
    })


    $("#modelSelectValue").change(function (e) {
        e.preventDefault();
        var select = document.getElementById("osSelectValue");
        var length = select.options.length;
        for (i = length - 1; i >= 1; i--) {
            select.options[i] = null;
        }


        var select = document.getElementById("seriesSelectValue");
        var length = select.options.length;
        for (i = length - 1; i >= 1; i--) {
            select.options[i] = null;
        }

        let model = $(this).val();
        let vendor = $('#vendorSelectValue').val();
        let device = $('#deviceSelectValue').val();
        $.ajax({
            type: 'GET',
            url: "items",
            data: { model: model, vendor: vendor, device: device, option: 'model' },
            headers: {
                'X-CSRFToken': "{{ csrf_token }}",
            },

            success: function (response) {

                osJson = {};
                osArray = [];
                for (osItem of response.operating_systems) {
                    osJson[modelItem] = osItem;
                    osArray.push(osItem);
                }
                var sel = document.getElementById('osSelectValue');
                for (var i = 0; i < osArray.length; i++) {
                    var opt = document.createElement('option');
                    opt.innerHTML = osArray[i];
                    opt.value = osArray[i];
                    sel.appendChild(opt);
                }
            }

        })
    })


    $("#osSelectValue").change(function (e) {
        e.preventDefault();
        var select = document.getElementById("seriesSelectValue");
        var length = select.options.length;
        for (i = length - 1; i >= 1; i--) {
            select.options[i] = null;
        }

        let os = $(this).val();
        let vendor = $('#vendorSelectValue').val();
        let device = $('#deviceSelectValue').val();
        let model = $('#modelSelectValue').val();

        $.ajax({
            type: 'GET',
            url: "items",
            data: { os: os, vendor: vendor, device: device, model: model, option: 'os' },
            headers: {
                'X-CSRFToken': "{{ csrf_token }}",
            },

            success: function (response) {

                seriesJson = {};
                seriesArray = [];
                for (seriesItem of response.serieses) {
                    seriesJson[modelItem] = seriesItem;
                    seriesArray.push(seriesItem);
                }
                var sel = document.getElementById('seriesSelectValue');
                for (var i = 0; i < seriesArray.length; i++) {
                    var opt = document.createElement('option');
                    opt.innerHTML = seriesArray[i];
                    opt.value = seriesArray[i];
                    sel.appendChild(opt);
                }
            }

        })
    })



    $('#seriesSelectValue').on('click', function (event) {
        event.preventDefault();
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        var select = document.getElementById("fileList");
        var length = select.options.length;
        for (i = length - 1; i >= 1; i--) {
            select.options[i] = null;
        }

        let vendor = $('#vendorSelectValue').val();
        let device = $('#deviceSelectValue').val();
        let model = $('#modelSelectValue').val();
        let os = $('#osSelectValue').val();
        let series = $(this).val();

        $.ajax({
            type: 'GET',
            url: "items",
            data: {
                "vendor": vendor,
                "device": device,
                "model": model,
                "os": os,
                "series": series,
                "option": "series"
            },
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function (response) {
                var firms = [];
                var statustime = [];
                for (item of response.firmware) {
                    if (item == 'empty') {
                        firms += "<br><center><li>" + "N/A" + "&nbsp;" + "&#10061;" + "</center></li>";
                    }
                    else {
                        firms += "<br><center><li>" + item + "</center></li>";

                    }
                }


                for (item of response.last_upgrade_time) {
                    let d = item;
                    var date = new Date(d * 1000);
                    var hours = date.getHours();
                    var minutes = "0" + date.getMinutes();
                    var seconds = "0" + date.getSeconds();
                    var formattedtime = date.toDateString();

                    var today = new Date();
                    var currentime = today.toDateString();


                    if (item !== 'empty' && String(formattedtime) === String(currentime)) {
                        statustime += "<br><center><li>" + hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2) + "<b>,</b> " + "<b>Today</b>" + "&nbsp;" + "&#8986;" + "</center></li>";
                    }
                    else if (item !== 'empty' && formattedtime !== statustime) {
                        statustime += "<br><center><li>" + hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2) + "<b>,</b> " + formattedtime + "&nbsp;" + "&#8987;" + "</center></li>";
                    }
                    else if (item === 'empty') {
                        statustime += "<br><center><li>" + "N/A" + "&nbsp;" + "&#10061;" + "</center></li>";
                    }
                }

                $('#firmware_table').html("\n" +
                    "        <table class=wrap-input100 col-lg-12; style=\"font-family: arial, sans-serif;\n" +
                    "  border-collapse: collapse;\n" +
                    "list-style:none;\" id=\"firmware_table\">\n" +
                    "                  <tr class=wrap-input100;>" +
                    "    <th style=\"border: 1px solid #dddddd;" +
                    "  text-align: center;\n" +
                    " \">Binaries</th>" +
                    "    <th style=\"border: 1px solid #dddddd;\n" +
                    "  text-align: center;\n" +
                    " \">Last Upgrade Time</th>\n" +
                    "  </tr>\n" +
                    "   <tr style=\"\">\n" +
                    "    <td style=\"border: 1px solid #dddddd;\n" +
                    "text-align: center;\">" + "<b>" + firms + " </b>" + "</td>" +
                    "    <td style=\"border: 1px solid #dddddd;" +
                    "  text-align: center;" +
                    " \">" + "<b>" +  statustime + "</b>" + " </td>\n" +

                    "  </tr>\n" +
                    "</table>\n");
                $("#renew").html('<button type="button" class="btn btn-default btn-sm">\n' +
                    '          <span class="fa fa-refresh"></span> Refresh\n' +
                    '        </button>');



            s3Json = {};
            s3Array = [];
            for (s3Item of response.drivers) {
                s3Json[s3Item] = s3Item;
                s3Array.push(s3Item);
            }
            var sel = document.getElementById('fileList');
            for (var i = 0; i < s3Array.length; i++) {
                var opt = document.createElement('option');
                opt.innerHTML = s3Array[i];
                opt.value = s3Array[i];
                sel.appendChild(opt);                    
            }



            },
            error: function () {
                Swal.fire({
                    type: 'error',
                    title: 'Something went wrong!',
                }).then((result) => {
                    window.location.href = '';
                })
            }
        })

    });



    //UPLOAD FORM
    $('#fwUploadButton').on('click', function (event) {
        event.preventDefault();
        let uploadedFile;
        let localFile = $("#id_file")[0].files
        let fileList = $("#fileList").val()
        
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;



        if(localFile.length !== 0 && fileList.length !== 0)
        {
            var progress = null

            Swal.fire({
                type: 'error',
                title: "Multi file can not be sended!",
                text:"Please select single file"
            }).then((result) => {
                    
                });
            progress.abort()
        }
        else if(localFile.length > 0)
        {
            uploadedFile = localFile
        }
        else if(fileList.length > 0)
        {
            uploadedFile = fileList
        }
        

        let vendor = $('#vendorSelectValue').val();
        let device = $('#deviceSelectValue').val();
        let model = $('#modelSelectValue').val();
        let os = $('#osSelectValue').val();
        let series = $('#seriesSelectValue').val();
        if(vendor == "" || device == "" || model == "" || os == "" | series == "")
        {
            Swal.fire({
                type: 'error',
                title: "Please Select all options!",
            }).then((result) => {
                    
                });
        }
        else {

        
        
        Swal.fire('Please wait');
        Swal.showLoading();

        var data = new FormData($('#fileForm').get(0));
        data.append("file", uploadedFile);
        data.append("vendor", vendor);
        data.append("device", device);
        data.append("model", model);
        data.append("os", os);
        data.append("series", series);

        $.ajax({
            type: "POST",
            url: "upload",
            data: data,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrftoken
            },

            success: function () {
                Swal.fire({
                type: 'success',
                title: "The file was uploaded successfully!",
            }).then((result) => {
                    
                });
                $('#seriesSelectValue').trigger('click')
            },
            error: function () {

            }
        })


        }
        
        
    })

    //ADD SERIES
    $('#sendButton').on("click", function (event) {
        Swal.fire('Please wait');
        Swal.showLoading();
        event.preventDefault();

        const vendor = $('#id_vendor').val() != '' ? $('#id_vendor').val() : $('#vendorSelectValue').val()
        const device = $('#id_device').val() != '' ? $('#id_device').val() : $('#deviceSelectValue').val()
        const model = $('#id_model').val() != '' ? $('#id_model').val() : $('#modelSelectValue').val()
        const series = $('#id_series').val() != '' ? $('#id_series').val() : $('#seriesSelectValue').val()
        const os = $('#id_operating_system').val() != '' ? $('#id_operating_system').val() : $('#osSelectValue').val()
        if (vendor === null || device === null || model === null || series === null || os === null) {
            Swal.fire({
                type: 'error',
                title: 'All options must be filled!',
            })
        }
        else {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            $.ajax({
                type: "POST",
                url: "driver",
                data: {
                    "vendor": vendor,
                    "device": device,
                    "model": model,
                    "series": series,
                    "os": os
                },
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (response) {
                    var msg = "Values added successfully!";
                    Swal.fire({
                        title: msg,
                        type: 'success',
                        showCloseButton: true,
                    }).then((result) => {
                    });
                },
                error: function (response) {
                    var msg = "Failed adding values";
                    if (response.status === 409)
                        msg = "The item already exists";
                    Swal.fire({
                        type: 'error',
                        title: msg,
                    }).then((result) => {
                        //window.location.href = '';
                    })
                },
            })
        }

    });

});



//DOWNLOAD DRIVER
$("#downloadButton").on("click", function (event) {
    Swal.fire('Please wait');
    Swal.showLoading();
    event.preventDefault();
    const vendor = $('#id_vendor').val() != '' ? $('#id_vendor').val() : $('#vendorSelectValue').val()
    const device = $('#id_device').val() != '' ? $('#id_device').val() : $('#deviceSelectValue').val()
    const model = $('#id_model').val() != '' ? $('#id_model').val() : $('#modelSelectValue').val()
    const series = $('#id_series').val() != '' ? $('#id_series').val() : $('#seriesSelectValue').val()
    const os = $('#id_operating_system').val() != '' ? $('#id_operating_system').val() : $('#osSelectValue').val()
    let data = {
        "vendor": vendor,
        "device": device,
        "model": model,
        "series": series,
        "os": os
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
        type: "POST",
        url: "download",
        data: data,
        headers: {
            'X-CSRFToken': csrftoken
        },

        success: function (data) {
            Swal.fire({
                type: 'success',
                title: "The file is downloaded successfully!",
            }).then((result) => {

            });
        },
        error: function () {
            Swal.fire({
                type: 'error',
                title: "Something Went Wrong,Please try Later!",
            }).then((result) => {

            });
        }
    })
})



//DELETE FIRMWARE
$("#deleteFwButton").on("click", function (event) {
    Swal.fire('Please wait');
    Swal.showLoading();
    event.preventDefault();
    const vendor = $('#id_vendor').val() != '' ? $('#id_vendor').val() : $('#vendorSelectValue').val()
    const device = $('#id_device').val() != '' ? $('#id_device').val() : $('#deviceSelectValue').val()
    const model = $('#id_model').val() != '' ? $('#id_model').val() : $('#modelSelectValue').val()
    const series = $('#id_series').val() != '' ? $('#id_series').val() : $('#seriesSelectValue').val()
    const os = $('#id_operating_system').val() != '' ? $('#id_operating_system').val() : $('#osSelectValue').val()
    let data = {
        "vendor": vendor,
        "device": device,
        "model": model,
        "series": series,
        "os": os
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
        type: "POST",
        url: "deletedriver",
        data: data,
        headers: {
            'X-CSRFToken': csrftoken
        },

        success: function (data) {

            Swal.fire({
                type: 'success',
                title: "Selected series's firmware is deleted successfully!",
            }).then((result) => {


            });
        },
        error: function () {

            Swal.fire({
                type: 'error',
                title: "Something Went Wrong,Please try Later!",
            }).then((result) => {

            });


        }
    })
})


//DELETE SERIES
$("#deleteSeriesButton").on("click", function (event) {
    Swal.fire('Please wait');
    Swal.showLoading();
    event.preventDefault();
    const vendor = $('#id_vendor').val() != '' ? $('#id_vendor').val() : $('#vendorSelectValue').val()
    const device = $('#id_device').val() != '' ? $('#id_device').val() : $('#deviceSelectValue').val()
    const model = $('#id_model').val() != '' ? $('#id_model').val() : $('#modelSelectValue').val()
    const series = $('#id_series').val() != '' ? $('#id_series').val() : $('#seriesSelectValue').val()
    const os = $('#id_operating_system').val() != '' ? $('#id_operating_system').val() : $('#osSelectValue').val()
    let data = {
        "vendor": vendor,
        "device": device,
        "model": model,
        "series": series,
        "os": os
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    $.ajax({
        type: "POST",
        url: "deleteseries",
        data: data,
        headers: {
            'X-CSRFToken': csrftoken
        },

        success: function (data) {
            Swal.fire({
                type: 'success',
                title: "Selected series is deleted successfully!",
            }).then((result) => {


            });
        },
        error: function () {
            Swal.fire({
                type: 'error',
                title: "Something Went Wrong,Please try Later!",
            }).then((result) => {

            });
        }
    })
})





$('#vendorTypeButton').on('click', function (event) {
    document.getElementById("vendorSelectValue").value = 'Select vendor';
    $("#vendorTypeDiv").show();
    $("#vendorSelectButton").show();
    $("#vendorSelectDiv").hide();
    $(this).hide();
});

$('#vendorSelectButton').on('click', function (event) {
    document.getElementById("id_vendor").value = '';
    $("#vendorTypeDiv").hide();
    $("#vendorTypeButton").show();
    $("#vendorSelectDiv").show();
    $(this).hide();
});


$('#deviceTypeButton').on('click', function (event) {
    document.getElementById("deviceSelectValue").value = 'Select device';
    $("#deviceTypeDiv").show();
    $("#deviceSelectButton").show();
    $("#deviceSelectDiv").hide();
    $(this).hide();
});

$('#deviceSelectButton').on('click', function (event) {
    document.getElementById("id_device").value = '';
    $("#deviceTypeDiv").hide();
    $("#deviceTypeButton").show();
    $("#deviceSelectDiv").show();
    $(this).hide();
});




$('#modelTypeButton').on('click', function (event) {
    document.getElementById("modelSelectValue").value = 'Select Model';
    $("#modelTypeDiv").show();
    $("#modelSelectButton").show();
    $("#modelSelectDiv").hide();
    $(this).hide();
});

$('#modelSelectButton').on('click', function (event) {
    document.getElementById("id_model").value = '';
    $("#modelTypeDiv").hide();
    $("#modelTypeButton").show();
    $("#modelSelectDiv").show();
    $(this).hide();
});

$('#osTypeButton').on('click', function (event) {
    document.getElementById("osSelectValue").value = 'Select OS';
    $("#osTypeDiv").show();
    $("#osSelectButton").show();
    $("#osSelectDiv").hide();
    $(this).hide();
});

$('#osSelectButton').on('click', function (event) {
    document.getElementById("id_operating_system").value = '';
    $("#osTypeDiv").hide();
    $("#osTypeButton").show();
    $("#osSelectDiv").show();
    $(this).hide();
});


$('#seriesTypeButton').on('click', function (event) {
    document.getElementById("seriesSelectValue").value = 'Select Series';
    $("#seriesTypeDiv").show();
    $("#seriesSelectButton").show();
    $("#seriesSelectDiv").hide();
    $(this).hide();
});

$('#seriesSelectButton').on('click', function (event) {
    document.getElementById("id_series").value = '';
    $("#seriesTypeDiv").hide();
    $("#seriesTypeButton").show();
    $("#seriesSelectDiv").show();
    $(this).hide();
});
