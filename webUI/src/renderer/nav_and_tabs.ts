import * as util from "./utility";

export function openTab(clickedBtn: HTMLElement){
  util.updateActive(clickedBtn);

  // TODO update monaco + images accordingly
  // if (clickedBtn.parentElement.id === 'groupALinks'){
  //   let mocotabs = document.getElementById('groupBLinks');
  //   openTab(<HTMLElement>mocotabs.childNodes[0]);
  // }
}

export function openFigure(clickedA:HTMLElement) {
  util.updateActive(clickedA);

  // TODO: Renaming figures does not work as intended yet
  clickedA.parentElement.childNodes.forEach(element => {
    (<HTMLElement>element).contentEditable = 'false';
  });
  if (clickedA.id != 'Project') { // 'Project' cannot be renamed by user
    clickedA.contentEditable = 'true';
  }

  // TODO update tabs accordingly
  // let modules = document.getElementById('groupALinks');
  // openTab(modules[0]);
}

export function genTabs(parent:HTMLElement, group_tab_id:string, cssstyle:string, tab_unique_names: string[], onOpen: (btn:HTMLElement) => any = null){
  let parent_links = util.genElement(parent, 'div', cssstyle, group_tab_id+'Link', '');
  for (let i = 0; i < tab_unique_names.length; i++) {
    let btn = util.genElement(parent_links, 'button', 'tablinks', tab_unique_names[i], tab_unique_names[i]);
    if (i==0){
      var selectedBtn = btn;
    }
    btn.onclick = (ev: MouseEvent) => { openTab(btn); if (onOpen) onOpen(btn); };
  }
  openTab(selectedBtn);
  if (onOpen) onOpen(selectedBtn);
  return parent_links;
}

// TODO should generate as many Fig-Elements as folders
// Allowing the user to rename a folder could lead to problems like "cannot rename open file"
// Maybe the user renames a .txt file, which uses the webUI as 'foldernames'
export function genFigureNav(parent:HTMLElement, nav_names:string[]) : HTMLElement[] {
  let figure_nav = util.genElement(parent, 'div', 'sidenav', 'sidenav', '');

  let first = util.genElement(figure_nav, 'a', '', 'Project', 'Project');
  first.onclick = (ev: MouseEvent) => {openFigure(first);}
  nav_names.forEach(element => {
    let child = util.genElement(figure_nav, 'a', '', '', element);
    child.onclick = (ev: MouseEvent) => {openFigure(child);}
  });
  openFigure(first)
  return [figure_nav, first];
}

/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function openDropdown() {
  document.getElementById("DropdownAddMenu").classList.toggle("show");
}


// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (let i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
  // if (event.target.parentElement.id === 'sidenav') {
  //   openFigure(event.target);
  //   console.log('clicked on sidenav');
  // }
}

export function genPlusDropDown(parent:HTMLElement) {
  let div_parent = util.genElement(parent, 'div', 'dropdown', '', '');
  let btn = util.genElement(div_parent, 'button', 'dropbtn', '', '+');
  btn.onclick = openDropdown; 
  let div_items = util.genElement(div_parent, 'div', 'dropdown-content', 'DropdownAddMenu', '');
  // let refBtn = util.genElement(div_items, 'button', '', 'addRef', 'Add reference');
  // refBtn.onclick = (ev: MouseEvent) => { return addTab('Reference') };
  let gridBtn= util.genElement(div_items, 'button', '', 'addGrid', 'Add grid');
  gridBtn.onclick = (ev: MouseEvent) => { return addTab('Grid') };
  let plotBtn = util.genElement(div_items, 'button', '', 'addPlot', 'Add plot');
  plotBtn.onclick = (ev: MouseEvent) => { return addTab('Plot') };

  return div_parent;
}

function addTab(type:string){
  let parent = document.getElementById("groupALink");

  // get current tab ids to create unqiue tab name
  let children = parent.childNodes;
  let current_tabs = <string[]>[];
  for (let i = 0; i < children.length; i++) {
    let child = <HTMLElement>children[i];
    current_tabs.push(child.id);
  }

  // give based on type and current tabs suitable id
  let tab_unique_name = type+'9';
  let name_list = [type+'8', type+'7', type+'6', type+'5', type+'4', type+'3', type+'2', type+'1']; 
  for (let i = 0; i < name_list.length; i++) {
    if (!current_tabs.some(x => x === name_list[i])) {
      tab_unique_name = name_list[i];
    }
  } 

  // TODO create folder (with default files in it)
  let btn = util.genElement(parent, 'button', 'tablinks', tab_unique_name, tab_unique_name);
  openTab(btn);
}

export function createDeleteButton(parent:HTMLElement) {
  let deleteBtn = util.genElement(parent, 'button', 'deleteButton', 'delBtn', 'Delete active Tab');
  deleteBtn.onclick = removeActiveTab;
  return deleteBtn;
}

export function createSaveButton(parent:HTMLElement) {
  let saveBtn = util.genElement(parent, 'button', 'saveButton', 'saveBtn', 'Save open file changes');
  saveBtn.onclick = saveActiveFiles;
  return saveBtn;
}

function removeActiveTab() {
  let parent = document.getElementById("groupALink");
  let children = parent.childNodes;
  for (let i = 0; i < children.length; i++) {
    let child = <HTMLElement>children[i]
    if (child.className.includes('active')) {
      if (child.id.includes('Combined')) {
        alert('Tab "Combined" cannot be deleted.')
      }
      else if (confirm('Are you sure you want to delete the active tab: "'+ child.id+'"? Deleting a tab cannot be undone.')) {
        child.remove();
        openTab(document.getElementById('Combined'));
        document.getElementById('delBtn').style.display = 'none';
        // TODO delete corresponding folder
      } else {
        // Do nothing!
      }
    }
  }
}

// TODO
function saveActiveFiles() {
  let parent = document.getElementById("groupALink");
  let children = parent.childNodes;
  for (let i = 0; i < children.length; i++) {
    let child = <HTMLElement>children[i]
    if (child.className.includes('active')) {
      if (child.id.includes('Combined')) {
        console.log('TODO');
      } else {
        // TODO save content AND Layout/design
      }
    }
  }
}

export function genTabHelper(parent:HTMLElement, active_nav:HTMLElement, figures_path:string) : HTMLElement {
  let tab_list = [];
  if (active_nav.textContent === 'Project') {
      tab_list = ['Combined'];
  } else {
      tab_list = util.getModuleTabs(figures_path + '/' + active_nav.textContent);
  }
  let top_tab = genTabs(parent, 'groupA', 'tab', tab_list, (btn:HTMLElement) => { showDeleteBtn(btn); });
  return top_tab;
}

function showDeleteBtn(clickedBtn:HTMLElement) {
  if (clickedBtn.id === 'Combined') {
      document.getElementById('delBtn').style.display = 'none';
  } else {
      document.getElementById('delBtn').style.display = 'block';
  }
}