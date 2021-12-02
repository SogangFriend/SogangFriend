let polygons = [];
let container = document.getElementById('map'); //지도를 담을 영역의 DOM 레퍼런스

let options = { //지도를 생성할 때 필요한 기본 옵션
    center: new kakao.maps.LatLng(center['lat'], center['lng']), //지도의 중심좌표.
    level: 6 //지도의 레벨(확대, 축소 정도)
};
let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
drawLocation(true);

map.setZoomable(false);
map.setDraggable(false);

var customOverlay = new kakao.maps.CustomOverlay({
    map: map,
    content: '<div style="padding: 5px; background:#fff;">' +
        '내 위치: ' + si + " " + gu + " " + dong +
        '</div>',
    position: new kakao.maps.LatLng(37.462932227677896, 126.899851798148), // 커스텀 오버레이를 표시할 좌표 - 항상 맵 위의 고정 위치에 띄울 방법...?
    xAnchor: 0, // 컨텐츠의 x 위치
    yAnchor: 13 // 컨텐츠의 y 위치
});
// 지도 확대 축소를 제어할 수 있는  줌 컨트롤을 생성합니다
let zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

function clickCheck(id) {
    for (let i = 0; i < polygons.length; i++) {
        polygons[i].setMap(null);
    }
    polygons = [];

    id === "gu" ? drawLocation(true)
        : drawLocation(false);
}

function drawLocation(guFlag) {
    let dongName = dong.slice(0, dong.length - 1);
    if (!guFlag) {
        for (let i = 0; i < data.length; i++) {
            if (data[i]['name'].includes(dongName)) {
                displayArea(guFlag, data[i]['coords']);
            }
        }
    } else {
        for (let i = 0; i < data.length; i++) {
            displayArea(guFlag, data[i]['coords']);
        }
    }

    for (let i = 0; i < polygons.length; i++) {
        polygons[i].setMap(map);
    }
}

function displayArea(guFlag, coordinates) {
    polygons.push(makeMultiPolygon(guFlag, coordinates));
}

function makeMultiPolygon(guFlag, coordinates) {
    let paths = [];
    $.each(coordinates, function (index, val) {
        let coordinates2 = [];

        $.each(val[0], function (index2, coordinate) {
            coordinates2.push(new kakao.maps.LatLng(coordinate[1], coordinate[0]));
        });
        paths.push(coordinates2);
    });

    return new kakao.maps.Polygon({
        path: paths,
        strokeWeight: 5,
        strokeColor: guFlag ? '#FFBB00' : '#ff5900',
        strokeOpacity: 1,
        strokeStyle: 'solid',
        fillColor: guFlag ? '#FFE271' : '#ff7d3c',
        fillOpacity: 0.5
    });
}

const tabList = document.querySelectorAll('.tab_menu .list li');
// const contents = document.querySelectorAll('.left .left_body .lb_profile');
let activeCont = ''; // 현재 활성화 된 컨텐츠 (기본:#tab1 활성화)

for (var i = 0; i < tabList.length; i++) {
    tabList[i].querySelector('.btn').addEventListener('click', function (e) {
        e.preventDefault();
        // 나머지 버튼 클래스 제거
        for (let j = 0; j < tabList.length; j++) {
            if(tabList[j].firstElementChild !== e.target) {
                tabList[j].classList.remove('is_on');
                let a = tabList[j].firstElementChild.getAttribute('href');
                let contents = document.querySelectorAll(a);
                for (let k = 0; k < contents.length; k++) {
                    // 나머지 컨텐츠 display:none 처리
                    contents[k].style.display = 'none';
                }
            }
        }

        // 버튼 관련 이벤트
        this.parentNode.classList.add('is_on');

        // 버튼 클릭시 컨텐츠 전환
        activeCont = this.getAttribute('href');
        let l = document.querySelectorAll(activeCont);

        for (let j = 0; j < l.length; j++) {
            l[j].style.display = 'block';
        }
    });
}

function createChatRoom() {
    Swal.fire({
        title: '새 채팅방 생성',
        html: '<input type="text" id="chat_name" class="swal2-input" placeholder="채팅방 이름">',
        confirmButtonText: '생성',
        focusConfirm: false,
        preConfirm: () => {
            const name = Swal.getPopup().querySelector('#chat_name').value;
            if (!name) {
                Swal.showValidationMessage('이름을 입력해주세요');
            }
            return {name: name}
        }
    }).then((result) => {
        let data = {'name': result.value.name,};
        let csrftoken = getCookie('csrftoken');
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            url: "/chat/new/",
            method: "POST",
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            dataType: 'json',
        }).done((data) => {
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
            });
            location.reload();
        }).fail((data, status, error) => {
            Swal.fire({
                icon: 'error',
                html: status + ": " + error,
                buttonsStyling: false,
                confirmButtonText: "확인",
                width: '672px',

                customClass: {
                    confirmButton: 'swal-register-btn',
                    popup: 'swal-custom-container'
                },
            });
        });
    });
}


function enterChatRoom(pk) {
    let csrftoken = getCookie('csrftoken');
    let data = {'room_pk': pk};
    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        url: "/chat/enter/",
        method: "POST",
        data: JSON.stringify(data),
        processData: false,
        contentType: false,
        dataType: 'json',
    }).done((data) => {
        sessionStorage.setItem('default', data['room_pk']);
        location.href = "/chat/";
    }).fail((data, status, error) => {
        Swal.fire({
            icon: 'error',
            html: "입장하실 수 없습니다.<br>"+status + " " + error,
            buttonsStyling: false,
            confirmButtonText: "확인",
            width: '672px',

            customClass: {
                confirmButton: 'swal-register-btn',
                popup: 'swal-custom-container'
            },
        });
    });
}


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}