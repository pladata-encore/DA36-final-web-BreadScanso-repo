document.addEventListener('DOMContentLoaded', function() {
    var storeName = "{{ store_name }}";
    var storeAddress = "{{ store_address|escapejs }}";

    // 매장에 따라 아이콘 변경
    var iconUrl = "{% static 'images/pink.png' %}";  // 기본 아이콘
    if (storeName === "강남점") {
        iconUrl = "{% static 'images/milk.png' %}";
    }

    // 주소를 좌표로 변환하는 함수
    naver.maps.Service.geocode({query: storeAddress},
        function(status, response) {
        if (status !== naver.maps.Service.Status.OK) {
            return alert('Something went wrong!');
        }
        var result = response.v2; // 검색 결과의 컨테이너
        var items = result.addresses; // 검색 결과의 배열

        var location = new naver.maps.LatLng(items[0].y, items[0].x);
        var map = new naver.maps.Map('map', {
            center: location,
            zoom: 17,
        });
        var marker = new naver.maps.Marker({
            position: location,
            map: map,
            icon:{
                url: iconUrl,
                scaledSize: new naver.maps.Size(60, 60),
                origin: new naver.maps.Point(0, 0),
                anchor: new naver.maps.Point(25, 26)
            }
        });
        var infowindow = new naver.maps.InfoWindow({
            content: '<div style="padding:7px;min-width:150px;line-height:100%;"><h5 style="margin-top:3px;">브레드스캔소 ' + storeName + '</h5></div>'
        });
        infowindow.open(map, marker);
    });
});
