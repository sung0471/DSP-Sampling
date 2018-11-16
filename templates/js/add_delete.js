var count=0;
function add_signal(){
    var formobj=document.getElementById("input_area");
    var lastDiv=document.getElementById(String(count));
    var newDiv=document.createElement("div");
    var newInput=new Array();
    var newBr=document.createElement("br");

    for(var i=0;i<3;i++)
        newInput[i]=document.createElement("input");

    count++;
    newDiv.id=String(count);
    newDiv.innerText="Frequency(Hz) : ";

    newInput[0].type="text";
    newInput[0].id="frequency["+String(count)+"]";
    newDiv.appendChild(newInput[0]);
    newDiv.innerHTML+=" Amplitude : ";

    newInput[1].type="text";
    newInput[1].id="amplitude["+String(count)+"]";
    newDiv.appendChild(newInput[1]);
    newDiv.innerHTML+=" Phase(Degree) : ";

    newInput[2].type="text";
    newInput[2].id="phase["+String(count)+"]";
    newDiv.appendChild(newInput[2]);

    newDiv.appendChild(newBr);
    formobj.append(newDiv);
}
function delete_signal(){
    if(count>-1){
        var lastDiv=document.getElementById(String(count));
        lastDiv.remove();
        count--;
    }
}
