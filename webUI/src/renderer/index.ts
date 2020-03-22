import "./css/main.css"; 
import "./css/sidenav.css"; 
import "./css/tab.css";
import "./css/dropdown.css"; 

import * as nat from "./nav_and_tabs";
import * as util from "./utility";
import * as moco from "./monaco";

let tab_list = ['Combined', 'Reference1', 'Grid1', 'Plot1'];

let nav = nat.genSideNav(document.body);
const mainbody = util.genElement(document.body, 'div', 'main', '', '');

nat.createDeleteButton(mainbody);
function showDeleteBtn(clickedBtn:HTMLElement) {
    if (clickedBtn.id === 'Combined') {
        document.getElementById('delBtn').style.display = 'none';
    } else {
        document.getElementById('delBtn').style.display = 'block';
    }
}  

let top_tab = nat.genTabs(mainbody, 'groupA', 'tab', tab_list, (btn:HTMLElement) => { showDeleteBtn(btn); });
nat.genPlusDropDown(top_tab);

const monaco_body = util.genElement(mainbody, 'div', 'half left', '', '');
nat.genTabs(monaco_body, 'groupB', 'tab1', ['Content', 'Config']);
mainbody.style.width = document.body.clientWidth - nav.clientWidth + 'px'; //needs to be resized before genMonaco
let mocoEditor = moco.genMonaco(monaco_body);

const img_viewer = util.genElement(mainbody, 'div', 'half right', '', '');





import { remote } from 'electron';
import * as fs from 'fs';

fs.readFile('C:/Users/admin/Documents/MasterThesis/mtc/webUI/src/images/svg_example_1.svg', (err, data) => {console.log(data);});

const temp = remote.app.getPath('temp');
// generate .svg or whatever in temp


let img = util.loadImage(img_viewer, 'file:///C:/Users/admin/Documents/MasterThesis/mtc/webUI/src/images/svg_example_1.svg');

import * as chproc from 'child_process';
const pygen = chproc.spawn('python', ['--version'])

pygen.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
});
  
pygen.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
});

pygen.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
});


function resize() {
    mainbody.style.width = document.body.clientWidth - nav.clientWidth + 'px'; //needs to be resized before genMonaco
    monaco_body.style.width = mainbody.clientWidth * 0.5 +'px';
    monaco_body.style.height = mainbody.clientHeight - top_tab.clientHeight - 2.0 + 'px';

    mocoEditor.layout();

    img_viewer.style.width = monaco_body.clientWidth +'px';
    img_viewer.style.height = monaco_body.clientHeight + 'px';
    img_viewer.style.position = 'fixed';
    img_viewer.style.left = monaco_body.clientWidth + nav.clientWidth + 'px';
    img_viewer.style.top = '45px';

    let width = 200;
    let height = 100;
    img.style.width = width + 'px';
    img.style.height = height + 'px';
    img.style.top = (img_viewer.clientHeight - height) * 0.5 + 'px';
    img.style.left = (img_viewer.clientWidth - width) * 0.5 + 'px';
}
resize();

var addEvent = function(object, type, callback) {
    if (object == null || typeof(object) == 'undefined') return;
    if (object.addEventListener) {
        object.addEventListener(type, callback, false);
    } else if (object.attachEvent) {
        object.attachEvent("on" + type, callback);
    } else {
        object["on"+type] = callback;
    }
};

addEvent(window, "resize", function(event) {
    resize();
});
