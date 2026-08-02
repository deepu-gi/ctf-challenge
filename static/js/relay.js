const output = document.getElementById("relay-output");
const input = document.getElementById("relay-command");

let cwd = "/";
let history = [];
let historyIndex = -1;

const filesystem = {

"/":[
"logs",
"keys",
"archive"
],

"/logs":[
"radio.log",
"transmission.log"
],

"/keys":[
"operator.key"
],

"/archive":[
"mission.txt"
]

};

const files = {

"/logs/radio.log":

`Recovered Signal

Operator still trusted Morse.

One fragment was transmitted separately.

Nothing else recovered.`,

"/logs/transmission.log":

`REP-7

Revision 7

Transmission verified.

Relay stable.`,

"/keys/operator.key":

`ZXhjZWVkZWQ=`,

"/archive/mission.txt":

`Mission Archive

Classified

Authorization Level

OPERATOR`

};

function print(text){

output.innerHTML+="<br>"+text;

output.scrollTop=output.scrollHeight;

}

function execute(cmd){

cmd=cmd.trim();

if(cmd==="")
return;

history.push(cmd);
historyIndex=history.length;

print("<span style='color:#6aff6a;'>relay@milnet:"+cwd+"$</span> "+cmd);

if(cmd==="help"){

print(`Commands

help

ls

pwd

cd

cat

whoami

clear

logout`);

return;

}

if(cmd==="pwd"){

print(cwd);

return;

}

if(cmd==="whoami"){

print("relay_operator");

return;

}

if(cmd==="ls"){

print(filesystem[cwd].join("<br>"));

return;

}

if(cmd.startsWith("cd ")){

let dir=cmd.substring(3).trim();

if(dir===".."){

cwd="/";

return;

}

let next=cwd==="/"
?"/"+dir
:cwd+"/"+dir;

if(filesystem[next]){

cwd=next;

return;

}

print("Directory not found.");

return;

}

if(cmd.startsWith("cat ")){

let file=cmd.substring(4).trim();

let path=cwd+"/"+file;

path=path.replace("//","/");

if(files[path]){

print(files[path]);

return;

}

print("File not found.");

return;

}

if(cmd==="clear"){

output.innerHTML="";

return;

}

if(cmd==="logout"){

window.location="/logout";

return;

}

print("Unknown command.");

}

input.addEventListener("keydown",function(e){

if(e.key==="Enter"){

execute(input.value);

input.value="";

}

});
