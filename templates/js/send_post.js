function send_data(check) {
    var url = "http://" + location.host + "/send";    // html을 호출한 Host와 똑같은 주소로 json파일 호출
    var serverSend = new XMLHttpRequest();      // file읽기 위한 http request 객체 생성
    var json_data={};
    var isCos = new Array();
    var frequency = new Array();
    var amplitude = new Array();
    var phase = new Array();
    var attr = new Array();

    for (var i = 0; i <= count; i++) {
        attr[0] = parseInt(document.getElementById("isCos[" + String(i) + "]").value);
        attr[1] = parseFloat(document.getElementById("frequency[" + String(i) + "]").value);
        attr[2] = parseFloat(document.getElementById("amplitude[" + String(i) + "]").value);
        attr[3] = parseFloat(document.getElementById("phase[" + String(i) + "]").value);
        for (j = 0; j < attr.length; j++)
            if (isNaN(attr[j]))
                attr[j] = 0;
        isCos[i] = attr[0];
        frequency[i] = attr[1];
        amplitude[i] = attr[2];
        phase[i] = attr[3];
        phase[i] = phase[i]*Math.PI/180;
    }

    json_data["index"] = count + 1;
    json_data["isCos"] = isCos;
    json_data["carrier_frequency"] = frequency;
    json_data["amplitude"] = amplitude;
    json_data["phase"] = phase;
    json_data["sampling_rate"]=parseFloat(document.getElementById("sampling_rate").value);

    serverSend.open('POST', url, true);          // url 열기
    serverSend.setRequestHeader("Content-type", "application/json");
    serverSend.send(JSON.stringify(json_data));

    var logobj=document.getElementById("printlog");
    logobj.innerHTML="Send data...";

    wait_request();
}