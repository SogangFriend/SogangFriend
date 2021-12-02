function name_overlap_check() {
    let nameInput = $('#name_input');
    nameInput.change(function () {
        $('#name_btn').show();
        $('#name_input').attr("check_result", "fail");
    })


    if (nameInput.val() === '') {
        alert('닉네임을 입력해주세요.')
        return;
    }

    let name_overlap_input = document.querySelector('input[name="name"]');

    $.ajax({
        url: "/member/check/",
        data: {
            'name': name_overlap_input.value
        },
        datatype: 'json',
        success: function (data) {
            if (data['overlap'] === "fail") {
                alert("이미 존재하는 닉네임 입니다.");
                name_overlap_input.focus();
            } else {
                alert("사용가능한 닉네임 입니다.");
                $('#name_input').attr("check_result", "success");
                $('#name_btn').show();
            }
        }
    });
}

let geocoder = new kakao.maps.services.Geocoder();
let lat, lng;

function coordToAddr() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            lat = position.coords.latitude;
            lng = position.coords.longitude;
            geocoder.coord2RegionCode(lng, lat, function (result, status) {
                if (status === kakao.maps.services.Status.OK) {
                    let addr = result[1].address_name.split(' ');
                    addr = addr[0] + " " + addr[1] + " " + addr[2];
                    document.getElementById("location").value = addr;
                    document.getElementById("location").readOnly = true;
                }
            });
        }, function (error) {
            console.error(error);
        }, {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: Infinity
        });
    } else {
        alert('GPS NOT SUPPORTED');
    }
}

function clicked() {
    let form = $('#register-form')[0];
    let formData = new FormData(form);
    $.ajax({
        url: "/member/new/",
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        dataType: 'json',
    })
        .done((data) => {
            if (data['success'] === 0) {
                Swal.fire({
                    icon: 'success',
                    html: data['message'],
                    buttonsStyling: false,
                    confirmButtonText: "확인",
                    width: '672px',

                    customClass: {
                        confirmButton: 'swal-register-btn',
                        popup: 'swal-custom-container'
                    },
                    footer: data['footer']
                });
            } else {
                if (data['success'] === 1) {
                    Swal.fire({
                        icon: 'error',
                        html: data['message'],
                        buttonsStyling: false,
                        confirmButtonText: "확인",
                        width: '672px',

                        customClass: {
                            confirmButton: 'swal-register-btn',
                            popup: 'swal-custom-container'
                        },
                        footer: data['footer']
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        html: data['message'],
                        buttonsStyling: false,
                        confirmButtonText: "로그인하러 가기",
                        cancelButtonText: "비밀번호 찾기",
                        width: '672px',
                        customClass: {
                            confirmButton: 'swal-register-btn',
                            cancelButton: 'swal-register-cancel-btn',
                            popup: 'swal-custom-container',
                        },
                        footer: data['footer']
                    })
                        .then((result) => {
                            if (result.isConfirmed) {
                                window.location = "/login/";
                            } else {
                                $.ajax({
                                    url: "/member/password/",
                                    method: "GET",
                                })
                            }
                        });
                }
            }

        })
        .fail(() => {
            console.log("failed");
        });
}


function numberMaxLength(e) {
    if (e.value.length > e.maxLength) {
        e.value = e.value.slice(0, e.maxLength);
    }
}