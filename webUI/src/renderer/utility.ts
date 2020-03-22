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