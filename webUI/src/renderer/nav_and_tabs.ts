import * as util from "./utility";

export function openTab(clickedBtn: HTMLElement){
  var tablinks = clickedBtn.parentElement.childNodes;
  for (var i = 0; i < tablinks.length; i++) {
    (<HTMLElement>tablinks[i]).className = (<HTMLElement>tablinks[i]).className.replace(" active", "");
  }
  clickedBtn.className += " active";
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

export function openSideNav(a:HTMLElement) {
  let sidenav = document.getElementById("sidenav");
  for (let i = 0; i<sidenav.childNodes.length; i++) {
    let child = <HTMLElement>sidenav.childNodes[i]
    child.className.replace(" active", "");
    child.contentEditable = 'false';
  }
  a.className += " active";
  if (a.id != 'Project') {
    a.contentEditable = 'true';
  }
}

// TODO should generate as many Fig-Elements as folders
// Allowing the user to rename a folder could lead to problems like "cannot rename open file"
// Maybe the user renames a .txt file, which uses the webUI as 'foldernames'
export function genSideNav(parent:HTMLElement) : HTMLElement {
  let sidenav = util.genElement(parent, 'div', 'sidenav', 'sidenav', '');

  let first = util.genElement(sidenav, 'a', '', 'Project', 'Project');
  let second = util.genElement(sidenav, 'a', '', '', 'Fig1');
  let third = util.genElement(sidenav, 'a', '', '', 'Fig2');
  let fourth = util.genElement(sidenav, 'a', '', '', '+');

  openSideNav(second)
  return sidenav;
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
}

export function genPlusDropDown(parent:HTMLElement) {
  let div_parent = util.genElement(parent, 'div', 'dropdown', '', '');
  let btn = util.genElement(div_parent, 'button', 'dropbtn', '', '+');
  btn.onclick = openDropdown; 
  let div_items = util.genElement(div_parent, 'div', 'dropdown-content', 'DropdownAddMenu', '');
  let refBtn = util.genElement(div_items, 'button', '', 'addRef', 'Add reference');
  refBtn.onclick = (ev: MouseEvent) => { return addTab('Reference') };
  let gridBtn= util.genElement(div_items, 'button', '', 'addGrid', 'Add grid');
  gridBtn.onclick = (ev: MouseEvent) => { return addTab('Grid') };
  let plotBtn = util.genElement(div_items, 'button', '', 'addPlot', 'Add plot');
  plotBtn.onclick = (ev: MouseEvent) => { return addTab('Plot') };

  return div_parent;
}

function addTab(type:string){
  let parent = document.getElementById("groupALink");

  // get current tab ids
  let children = parent.childNodes;
  let current_tabs = <string[]>[];
  for (let i = 0; i < children.length; i++) {
    let child = <HTMLElement>children[i];
    current_tabs.push(child.id);
  }

  // give based on type and current tabs suitable id
  let tab_unique_name = type+'8';
  let name_list = [type+'7', type+'6', type+'5', type+'4', type+'3', type+'2', type+'1']; 
  for (let i = 0; i < name_list.length; i++) {
    if (!current_tabs.some(x => x === name_list[i])) {
      tab_unique_name = name_list[i];
    }
  }
  
  let btn = util.genElement(parent, 'button', 'tablinks', tab_unique_name, tab_unique_name);
  openTab(btn);
}

export function createDeleteButton(parent:HTMLElement) {
  let deleteBtn = util.genElement(parent, 'button', 'deleteButton', 'delBtn', 'Delete active Tab');
  deleteBtn.onclick = removeActiveTab;
  return deleteBtn;
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
        // TODO delete
        child.remove();
        openTab(document.getElementById('Combined'));
        document.getElementById('delBtn').style.display = 'none';
      } else {
        // Do nothing!
      }
    }
  }
}