var MusicString = window.localStorage.getItem("musicinput");
var Bars = window.localStorage.getItem("barsinput");
var Error = window.localStorage.getItem("anyerrors");


/*if (!MusicString) {
	console.log("MusicString = " + MusicString);
}*/


function Initial(){
	MusicString = 0;
	Bars = 0;
	Error = 0;
	console.log("MusicString = " + MusicString);
	console.log("Bars = "+ Bars);
	console.log("Error = "+ Error);
}

function ChangeBars() {
    Bars = parseInt(document.getElementById("Bars").value);
	console.log("Bars = "+ Bars);
	if (!(Bars >= 0 || Bars < 0)) {
		alert("SOMETHING BROKE");
	}
}

function ProvideNotesInterface() {
	var header2 = '&nbsp;&nbsp;&nbsp;';
    var header3 = '<select id="';
    var header4 = '" size="12">\n';
    var body0 = '<option value="0">A</option>\n<option value="1">A#</option>\n<option value="2">B</option>\n<option value="3">C</option>\n';
    var body1 = '<option value="4">C#</option>\n<option value="5">D</option>\n<option value="6">D#</option>\n<option value="7">E</option>\n';
	var body2 = '<option value="8">F</option>\n<option value="9">F#</option>\n<option value="10">G</option>\n<option value="11">G#</option>';
    var footer = '</select>&nbsp;&nbsp;&nbsp;'; //Add rests, change to hexadecimal
    var complete ='';

	for (var i = 0; i < Bars; i++) {
	    complete += i + header2 +header3 + i + header4 + body0 + body1 + body2 + footer;
	}
    document.getElementById('NotesInterface').innerHTML = complete;
    //Formatting
    //Limit number of dropdowns per row
}

function MelodyInput() {
	MusicString = "";
    for (var i = 0; i < Bars; i++) {
    	MusicString += document.getElementById(i).value;
    }
	console.log(MusicString);
}

function MelodyOutput() {
	console.log(MusicString);
}