import React from 'react';
import Button from '@material-ui/core/Button';
import './Result.css';
import MapStateToProps from "./MapStateToProps";

import { connect } from "react-redux";

function ResultTemplate(props) {

  return (
    <div className="container">
      <div className="editor-buttons-row">
        <div className="buttons-block">
          <div className="button set-grammar-button">
            <Button variant="contained" color="primary" disabled={!props.changingGrammarActive} onClick={props.onClickSetGrammar}>Set grammar</Button>
          </div>
          <div className="button change-grammar-button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickChangeGrammar}>Change grammar</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickSyntaxDiagram}>Syntax diagram</Button>
          </div>
        </div>

        <div className="buttons-block">
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickAST}>AST</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickInterpreter}>INTERPRETER</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickCode}>Code</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickDiagram}>Diagram</Button>
          </div>
        </div>
      </div>
      <div className="row error" id="errorMsg">
        {props.error.value}
      </div>
    </div>
  )
}

export default connect(MapStateToProps) (ResultTemplate)
