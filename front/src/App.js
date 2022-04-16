import React, { useRef, useState } from 'react';
import SplitPane from 'react-split-pane';
import Pane from 'react-split-pane/lib/Pane';
import { SourceCode } from './components/SourceCode'
import { Result } from './components/Result'
import logo from './logo.svg';
import './App.css';

import "ace-builds/src-noconflict/mode-java";
import "ace-builds/src-noconflict/theme-github";

function onChange(newValue) {
  console.log("change", newValue);
}

function save(sourceCodeExample, syntaxExample, semanticsExample) {
  localStorage.setItem("sourceCodeExample", sourceCodeExample)
  localStorage.setItem("syntaxExample", syntaxExample)
  localStorage.setItem("semanticsExample", semanticsExample)
}


function App() {
  const refLU = useRef(null)
  const refLD = useRef(null)
  const refRU = useRef(null)

  const sourceCodeExample =
    `( [ + {shape=circle} ]

  < 0 {color=red} >
  ( [ A ] )

  < 1 >
  ( [ * ]

    < 0 >
    ( [ B ] )

    < 1 >
    ( [ C ] )
  )
)`

  const syntaxExample =
    `grammar ASTgrammar;
    t : '(' n (l t )* ')';
    n : '[' txt  (c )* ']';
    l : '<' txt  (c )* '>';
    c : '{' txt '=' txt '}';
    txt : SYMBOL ( SYMBOL)*;
    SPACE: [ \\t\\r\\n] -> skip;
    SYMBOL: ~( '(' | ')' | '[' | ']' | '<' | '>' | '{' | '}' );`

  const semanticsExample =
    `Tree
VAR
  entryTreeFlag := False
  exitTreeFlag := False
  tree := ""
  node := ""
  link := ""
REQUIRED
  nextNode(x)
  nextLink(x)
  popNodesStack()
  node.entryNode()
  node.ifExitNode()
  link.entryLink()
  link.ifExitLink()
PROVIDED
  entryTree()
  ifExitTree()
STATE
  entry -> entryTreeFlag / node := nextNode(tree) -> start_node
  start_node -> True / node.entryNode() -> end_node
  end_node -> node.ifExitNode() /  -> get_link
  get_link -> True / link := nextLink(tree) -> check_link
  check_link -> link != "" / link.entryLink() -> end_link
  end_link -> link.ifExitLink() /  -> get_link
  check_link -> else / popNodesStack() -> end_tree
  end_tree -> True / exitTreeFlag := True -> exit


Node
VAR
  entryNodeFlag := False
  exitNodeFlag := False
  node := ""
REQUIRED
  popLinkStack()
  pushNodesStack(x)
  sizeNodeStack()
PROVIDED
  entryNode()
  ifExitNode()
INNER
  printNode()
  printLink(link)
STATE
  entry -> entryNodeFlag / pushNodesStack(node) -> print_node
  print_node -> True / printNode() -> check_link
  check_link -> sizeNodesStack() > 1 / printLink(popLinkStack()) -> end_node
  end_node -> True / exitNodeFlag := True -> exit
  check_link -> else / exitNodeFlag := True -> exit


Link
VAR
  entryLinkFlag := False
  exitLinkFlag := False
  link := ""
  tree := ""
REQUIRED
  nextTree(x)
  pushLinkStack(link)
  tree.entryTree()
  tree.ifExitTree()
PROVIDED
  entryLink()
  ifExitLink()
STATE
  entry -> entryLinkFlag / pushLinkStack(link) -> get_tree
  get_tree -> True / tree := nextTree(link) -> start_tree
  start_tree -> True / tree.entryTree() -> end_tree
  end_tree -> tree.ifExitTree() / exitLinkFlag := True -> exit
`

  const editorOnResize = (...refs) => (e) => {
    refs.forEach((ref) => { ref.current.editor.resize() })
  }

  const SERVER_URL = process.env.REACT_APP_SERVER_URL
  const FRONT_URL = process.env.REACT_APP_FRONT_URL
  
  const AST_URL = SERVER_URL + '/ast'
  const INTERPRETER_URL = SERVER_URL + '/interpreter'
  const FILES_URL = SERVER_URL + '/files' 
  const CODE_URL = SERVER_URL + '/code' 

  const error = {
    value: ''
  }

  const onClickAST = async (e) => {
    save(refLU.current.editor.getValue(),
    refLD.current.editor.getValue(),
    refRU.current.editor.getValue())
    
    console.log('Sending request to build AST ' + AST_URL)

    let request = await fetch(AST_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        "source": refLU.current.editor.getValue(),
        "syntax": refLD.current.editor.getValue()
      })
    });

    let response = await request.json();
    console.log(response)
    // console.log(JSON.parse(response))
    // let result = JSON.parse(response)
    if (response.error === 0) {
      console.log('Opening ' + FILES_URL + '/' + response.info)
      window.open(FILES_URL + '/' + response.info)
      document.getElementById('errorMsg').innerText = ""
    }
    else {
      document.getElementById('errorMsg').innerText = response.info
    }
  }

  const onClickInterpreter = async (e) => {
    save(refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue())

    console.log('Sending request to build interpreter ' + INTERPRETER_URL)

    let request = await fetch(INTERPRETER_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        "source": refLU.current.editor.getValue(),
        "syntax": refLD.current.editor.getValue()
      })
    }
    );

    let response = await request.json();
    if (response.error === 0) {
      console.log('Opening ' + FILES_URL + '/' + response.info)
      window.open(FILES_URL + '/' + response.info)
      document.getElementById('errorMsg').innerText = ""
    }
    else {
      document.getElementById('errorMsg').innerText = response.info
    }
  }

  const onClickCode = async (e) => {
    save(refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue())

    console.log('Sending request to build interpreter ' + CODE_URL)

    let request = await fetch(CODE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        "symantic": refRU.current.editor.getValue()
      })
    }
    );

    let response = await request.json();
    console.log(response)
    // console.log(JSON.parse(response))
    // let result = JSON.parse(response)
    if (response.error === 0) {
      console.log('Opening ' + FILES_URL + '/' + response.info)      
      window.open(FILES_URL + '/' + response.info)
      document.getElementById('errorMsg').innerText = ""
    }
    else {
      document.getElementById('errorMsg').innerText = response.info
    }
  }

  const onClickDiagram = async (e) => {
    save(refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue())
    let request = await fetch(SERVER_URL + '/diagram', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        "symantic": refRU.current.editor.getValue()
      })
    }
    );

    let response = await request.json();
    // console.log(response)
    // console.log(JSON.parse(response))
    // let result = JSON.parse(response)
    if (response.error === 0) {
      console.log('Opening ' + FILES_URL + '/' + response.info)
      window.open(FILES_URL + '/' + response.info)
      document.getElementById('errorMsg').innerText = ""
    }
    else {
      document.getElementById('errorMsg').innerText = response.info
    }
  }


  return (
    <div className="App">
      <SplitPane
        split="vertical"
        onChange={editorOnResize(refLU, refLD, refRU)}
      >
        <SplitPane
          split="horizontal"
          onChange={editorOnResize(refLU, refLD)}
        >
          <Pane>
            <SourceCode fRef={refLU} value={localStorage.getItem("sourceCodeExample") ? localStorage.getItem("sourceCodeExample") : sourceCodeExample} />
          </Pane>
          <Pane>
            <SourceCode fRef={refLD} value={localStorage.getItem("syntaxExample") ? localStorage.getItem("syntaxExample") : syntaxExample} />
          </Pane>
        </SplitPane>
        <SplitPane
          split="horizontal"
          onChange={editorOnResize(refRU)}
        >
          <Pane initialSize="85%">
            <SourceCode fRef={refRU} value={localStorage.getItem("semanticsExample") ? localStorage.getItem("semanticsExample") : semanticsExample} />
          </Pane>
          <Pane>
            <Result onClickAST={onClickAST} onClickInterpreter={onClickInterpreter} onClickCode={onClickCode} onClickDiagram={onClickDiagram} error={error} />
          </Pane>
        </SplitPane>
      </SplitPane>
    </div>
  );
}

export default App;
