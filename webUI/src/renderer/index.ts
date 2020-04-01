import "./css/main.css"; 
import "./css/sidenav.css"; 
import "./css/tab.css";
import "./css/dropdown.css"; 

import * as nat from "./nav_and_tabs";
import * as util from "./utility";
import * as moco from "./monaco";

// PATHS & FILENAMES 
const workDir_path = 'C:/Users/admin/Documents/MasterThesis/mtc/workDir'; // changes once
const figures_path = workDir_path + '/figures' // fix
const spez_fig_path = figures_path + '/fig1' // changes
const module_path = spez_fig_path + '/grid1' // changes 

const content_filename = 'content.py'
const config_filename = 'layout_and_design.json'
const png_filename = 'gen_png_file.png'
const manage_images_file = 'manage_images.py'
// PATHS & FILENAMES END

// HTML ELEMENTs
let nav_and_active_nav = nat.genFigureNav(document.body, util.getFigureNavs(figures_path));
let nav = nav_and_active_nav[0];
let active_nav = nav_and_active_nav[1];
const mainbody = util.genElement(document.body, 'div', 'main', '', '');

nat.createDeleteButton(mainbody);
// showDeleteBtn  

let top_tab = nat.genTabHelper(mainbody, active_nav, figures_path);

// MONACO body/tabs
const monaco_body = util.genElement(mainbody, 'div', 'half left', '', '');
if (active_nav.textContent !== 'Project') {
    nat.genPlusDropDown(top_tab);
    nat.genTabs(monaco_body, 'groupB', 'tab1', ['Content', 'Layout and design']);
} else {
    nat.genTabs(monaco_body, 'groupB', 'tab1', ['Manage Images']);
}
mainbody.style.width = document.body.clientWidth - nav.clientWidth + 'px'; //needs to be done before genMonaco
let mocoEditor = moco.genMonaco(monaco_body);
// MONACO body/tabs end

const img_viewer = util.genElement(mainbody, 'div', 'half right', '', '');
let img = util.loadImage(img_viewer, 'file:///'+ module_path +'/'+ png_filename);
// HTML ELEMENTS END

// LOAD FILE (Monaco)
import { remote } from 'electron';
import * as fs from 'fs';

let open_file = '';
if (active_nav.textContent === 'Project'){
    open_file = workDir_path + '/' + manage_images_file;
} else {
    open_file = module_path + '/' + content_filename;
}

fs.readFile(open_file, 'utf8', (err, res) => {
    if (!err) { 
        mocoEditor.setModel(moco.makeMocoModel(res, 'python'));
    } else {
        // TODO ERROR HANDLING
    }
});
// fs.writeFile(open_file, mocoEditor.getValue(), (err) => {
//     if (err) {
//         TODO
//         console.log(err)
//     } else {
//         console.log('Saved changes.')
//     }
// })
// LOAD FILE END

// PYTHON CALL
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
// PYTHON CALL END

// RESIZE FUNCTIONS
function resizeImage() {
    if (img.naturalHeight == 0 || img.naturalWidth == 0)
        return;

    let width = img.naturalWidth;
    let height = img.naturalHeight;

    let factor = 1.0;
    while (width * factor > img_viewer.clientWidth || height * factor > img_viewer.clientHeight) {
        factor = factor - 0.05;
    }
    width = width * factor
    height = height * factor
    img.style.width = width + 'px';
    img.style.height = height + 'px';
    img.style.top = (img_viewer.clientHeight - height) * 0.5 + 'px';
    img.style.left = (img_viewer.clientWidth - width) * 0.5 + 'px';
}

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

    resizeImage()
}

img.onload = resizeImage;
resize();

util.addEvent(window, "resize", function(event) {
    resize();
});
// RESIZE FUNCTIONS END