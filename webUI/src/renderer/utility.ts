export function genElement(parent:HTMLElement, type:string, className:string, id:string, textContent:string) : HTMLElement {
  let elem = document.createElement(type);
  elem.className = className;
  elem.textContent = textContent;
  elem.id = id;
  parent.appendChild(elem);
  return elem;
}

export function loadImage(parent:HTMLElement, path:string){
  let img = <HTMLImageElement>genElement(parent, 'img', 'image', '', '');
  img.src = path;

  return img;
}

export function updateActive(clicked_element: HTMLElement) {
  clicked_element.parentElement.childNodes.forEach(element => {
    (<HTMLElement>element).className = (<HTMLElement>element).className.replace(" active", "");
  });
  clicked_element.className += " active";
}

export function addEvent(object, type, callback) {
  if (object == null || typeof(object) == 'undefined') 
    return;
  if (object.addEventListener) {
      object.addEventListener(type, callback, false);
  } else if (object.attachEvent) {
      object.attachEvent("on" + type, callback);
  } else {
      object["on"+type] = callback;
  }
};

// SEARCH FOR TABS/NAV FOLDER
import { remote } from 'electron';
import * as fs from 'fs';

export function getModuleTabs(path:string) : string[]{
  let files = fs.readdirSync(path);
  let tabs = [];
  files.forEach(element => {
    if (element.includes('combined') || element.includes('grid') || element.includes('plot')) {
      tabs.push(element);
    }
  });
  return tabs
}

export function getFigureNavs(path:string) : string[]{
  let files = fs.readdirSync(path);
  let figures = [];
  files.forEach(element => {
    figures.push(element);
  });
  return figures;
}

export function allCapitalizeFirstLetter(strings:string[]) : string[]{
  let newStrings = [];
  strings.forEach(element => {
    newStrings.push(capitalizeFirstLetter(element));
  });
  return newStrings;
}

export function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export function removeChilds(node:HTMLElement) {
  let last;
  while (last = node.lastChild) node.removeChild(last);
};

export function addChildren(parent:HTMLElement, children:string[], onclickfunction: (e: HTMLElement) => any) {
  children.forEach(child => {
    // TODO OR react
  });
}