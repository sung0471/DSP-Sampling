function wait_request() {
    var url = "http://" + location.host + "/send";  // html을 호출한 Host와 똑같은 주소로 json파일 호출
    var fileReader = new XMLHttpRequest();          // file읽기 위한 http request 객체 생성
    fileReader.onload = function () {            // 읽었을 경우 실행하는 함수
        if (fileReader.status == 200) {         // 읽는게 성공하면
            var logobj=document.getElementById("printlog");
            logobj.innerHTML+="<br>Printing Graph...";

            var version = JSON.parse(fileReader.responseText);   // 읽은 Text를 JSON문법으로 파싱, 저장
            var plotarea=document.getElementsByClassName("plot")[0];
            if(plotarea.childElementCount>0) {
                var imgobj = document.getElementById("plot");
                plotarea.removeChild(imgobj);
            }
            var date=new Date();
            var imgobj = new Image();
            imgobj.id = "plot";
            imgobj.setAttribute("height","90%");
            imgobj.src="figures/result"+String(version["version"])+".svg";
            plotarea.appendChild(imgobj);

            logobj.innerHTML+="<br>Finish Sampling!";
        }
    };
    fileReader.open('GET', url, true);          // url 열기
    fileReader.send(null);
}