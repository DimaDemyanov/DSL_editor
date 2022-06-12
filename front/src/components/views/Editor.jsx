import React, { useRef } from 'react';
import SplitPane from 'react-split-pane';
import Pane from 'react-split-pane/lib/Pane';
import { Provider } from 'react-redux';
import { SourceCode } from '../SourceCode';
import ProgramSourceCode from '../SourceCode/ProgramSourceCode';
import GrammarSourceCode from '../SourceCode/GrammarSourceCode';
import Result from '../Result/Result';
import fetchPostJson, { getCookieByName } from '../../utilities/Queries';

import 'ace-builds/src-noconflict/mode-java';
import 'ace-builds/src-noconflict/theme-github';

import store from '../../store';
import { LocalStorage } from '../../helpers/localStorage';

function openResource(path) {
  console.log(`Opening ${FILES_URL}/dsls/${getCookieByName('username')}/${getCookieByName('project')}/public/${path}`);
  window.open(`${FILES_URL}/dsls/${getCookieByName('username')}/${getCookieByName('project')}/public/${path}`);
}

const SERVER_URL = process.env.REACT_APP_SERVER_URL;
//   const FRONT_URL = process.env.REACT_APP_FRONT_URL

const AST_URL = `${SERVER_URL}/ast`;
const SYNTAX_DIAGRAM_URL = `${SERVER_URL}/syntax-diagram`;
const INTERPRETER_URL = `${SERVER_URL}/interpreter`;
const FILES_URL = `${SERVER_URL}/files`;
const CODE_URL = `${SERVER_URL}/code`;
const DIAGRAM_URL = `${SERVER_URL}/diagram`;
const CHECK_GRAMMAR_URL = `${SERVER_URL}/check-grammar`;

function Editor() {
  const refLU = useRef(null);
  const refLD = useRef(null);
  const refRU = useRef(null);

  const editorOnResize = (...refs) => (e) => {
    refs.forEach((ref) => { ref.current.editor.resize(); });
  };

  const error = {
    value: '',
  };

  const onClickSetGrammar = async (e) => {
    LocalStorage.save(
      refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue(),
    );

    const response = await fetchPostJson(CHECK_GRAMMAR_URL, JSON.stringify({
      source: refLU.current.editor.getValue(),
      syntax: refLD.current.editor.getValue(),
    }));

    console.log(`Respone for setGrammar received: ${JSON.stringify(response)}`);

    if (response.error === 0) {
      store.dispatch({ type: 'WRITING_PROGRAM' });
      document.getElementById('errorMsg').innerText = '';
    } else {
      document.getElementById('errorMsg').innerText = response.error;
    }
  };

  const onClickChangeGrammar = async (e) => {
    LocalStorage.save(
      refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue(),
    );

    store.dispatch({ type: 'WRITING_GRAMMAR' });
  };

  const onClickSyntaxDiagram = async (e) => {
    LocalStorage.save(
      refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue(),
    );

    console.log(`Sending request to render syntax diagram ${SYNTAX_DIAGRAM_URL}`);

    const response = await fetchPostJson(SYNTAX_DIAGRAM_URL, JSON.stringify({
      syntax: refLD.current.editor.getValue(),
    }));

    if (response.error === 0) {
      openResource(response.info);
      document.getElementById('errorMsg').innerText = '';
    } else {
      document.getElementById('errorMsg').innerText = response.info;
    }
  };

  const onClickAST = async (e) => {
    LocalStorage.save(
      refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue(),
    );

    console.log(`Sending request to build AST ${AST_URL}`);

    const response = await fetchPostJson(AST_URL, JSON.stringify({
      source: refLU.current.editor.getValue(),
      syntax: refLD.current.editor.getValue(),
    }));

    if (response.error === 0) {
      openResource(response.info);
      document.getElementById('errorMsg').innerText = '';
    } else {
      document.getElementById('errorMsg').innerText = response.info;
    }
  };

  const onClickInterpreter = async (e) => {
    LocalStorage.save(
      refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue(),
    );

    console.log(`Sending request to build interpreter ${INTERPRETER_URL}`);

    const response = await fetchPostJson(INTERPRETER_URL, JSON.stringify({
      source: refLU.current.editor.getValue(),
      syntax: refLD.current.editor.getValue(),
    }));

    if (response.error === 0) {
      openResource(response.info);
      document.getElementById('errorMsg').innerText = '';
    } else {
      document.getElementById('errorMsg').innerText = response.info;
    }
  };

  const onClickCode = async (e) => {
    LocalStorage.save(
      refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue(),
    );

    console.log(`Sending request to build interpreter ${CODE_URL}`);

    const response = await fetchPostJson(CODE_URL, JSON.stringify({
      symantic: refRU.current.editor.getValue(),
    }));

    if (response.error === 0) {
      openResource(response.info);
      document.getElementById('errorMsg').innerText = '';
    } else {
      document.getElementById('errorMsg').innerText = response.info;
    }
  };

  const onClickDiagram = async (e) => {
    LocalStorage.save(
      refLU.current.editor.getValue(),
      refLD.current.editor.getValue(),
      refRU.current.editor.getValue(),
    );

    const response = await fetchPostJson(DIAGRAM_URL, JSON.stringify({
      symantic: refRU.current.editor.getValue(),
    }));

    if (response.error === 0) {
      openResource(response.info);
      document.getElementById('errorMsg').innerText = '';
    } else {
      document.getElementById('errorMsg').innerText = response.info;
    }
  };

  return (
    <Provider store={store}>
      <div className="App">
        <Result
          onClickSetGrammar={onClickSetGrammar}
          onClickChangeGrammar={onClickChangeGrammar}
          onClickSyntaxDiagram={onClickSyntaxDiagram}
          onClickAST={onClickAST}
          onClickInterpreter={onClickInterpreter}
          onClickCode={onClickCode}
          onClickDiagram={onClickDiagram}
          error={error}
        />
        <SplitPane
          className="editors-container"
          split="vertical"
          onChange={editorOnResize(refLU, refLD, refRU)}
        >
          <SplitPane
            split="horizontal"
            onChange={editorOnResize(refLU, refLD)}
          >
            <Pane>
              <ProgramSourceCode className="sourceCode" fRef={refLU} value={localStorage.getItem('sourceCode')} />
            </Pane>
            <Pane>
              <GrammarSourceCode className="syntax" fRef={refLD} value={localStorage.getItem('syntax')} />
            </Pane>
          </SplitPane>
          <SplitPane
            split="horizontal"
            onChange={editorOnResize(refRU)}
          >
            <Pane>
              <SourceCode className="semantics" fRef={refRU} value={localStorage.getItem('semantics')} />
            </Pane>
          </SplitPane>
        </SplitPane>
      </div>
    </Provider>
  );
}

export default Editor;
