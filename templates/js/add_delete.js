var count=0;
function add_signal(){
    var formobj=document.getElementById("input_area");
    var newDiv=document.createElement("div");

    var newSelect=document.createElement("select");
    var newOption=new Array();
    var newInput=new Array();
    var newBr=document.createElement("br");

    for(var i=0;i<3;i++)
        newInput[i]=document.createElement("input");

    count++;
    newDiv.id=String(count);
    
    newDiv.innerHTML="Cos or Sin : ";
    newSelect.id="isCos["+String(count)+"]";
    for(var i=0;i<2;i++){
        newOption[i]=document.createElement("option");
        newOption[i].value=String(i);
        if(i==0)
            newOption[i].innerHTML="Cosine";
        else
            newOption[i].innerHTML="Sin";
        newSelect.appendChild(newOption[i]);
    }
    newDiv.appendChild(newSelect);
    
    newDiv.innerHTML+=" Frequency(Hz) : ";
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
