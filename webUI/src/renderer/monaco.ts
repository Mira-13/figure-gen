import * as monaco from "monaco-editor"
import * as util from "./utility";

// TODO Monaco should load a file and show its content, allowing the user to edit the file
export function genMonaco(parent:HTMLElement) {
  let container = util.genElement(parent, 'div', 'monaco-container', 'monaco-container', '');
  container.style.height = '100%';

  return monaco.editor.create(container, {
    value: [
      'function x() {',
      '\tconsole.log("Hello world!");',
      '}'
    ].join('\n'),
    language: 'python'
  });
}